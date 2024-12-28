"""Parquet utilities.

This module provides utilities for working with Parquet files.
"""
from __future__ import annotations

import logging
from collections import deque
from typing import TYPE_CHECKING

import pandas as pd
import pyarrow as pa

# import pyarrow.parquet as pq
import pyarrow.dataset as ds
import s3fs
from fsspec.implementations.arrow import ArrowFSWrapper
from pyarrow import fs
from pytz import utc

from wvutils.path import stringify_path

if TYPE_CHECKING:
    from typing import Any

    from wvutils.type_aliases import FilePath

__all__ = [
    "get_parquet_session",
    "clear_parquet_sessions",
    "create_pa_schema",
    "force_dataframe_dtypes",
    "export_dataset",
]

logger: logging.Logger = logging.getLogger(__name__)


def _get_pa_type(type_name: str) -> pa.DataType:
    if type_name == "string":
        return pa.string()
    elif type_name == "integer":
        return pa.int64()
    elif type_name == "float":
        return pa.float64()
    elif type_name == "bool":
        return pa.bool_()
    elif type_name == "timestamp[s]":
        return pa.timestamp("s", tz=utc)
    elif type_name == "timestamp[ms]":
        return pa.timestamp("ms", tz=utc)
    elif type_name == "timestamp[ns]":
        return pa.timestamp("ns", tz=utc)
    else:
        raise ValueError(f"Unknown type name: {type_name!r}")


def create_pa_schema(schema_template: dict[str, str]) -> pa.schema:
    """Create a parquet schema from a template.

    Example:

    ```python
    {
        "key_a": "string",
        "key_b": "integer",
        "key_c": "float",
        "key_d": "bool",
        "key_e": "timestamp[s]",
        "key_f": "timestamp[ms]",
        "key_g": "timestamp[ns]",
    }
    ```

    becomes

    ```python
    pa.schema([
        ("key_a", pa.string()),
        ("key_b", pa.int64()),
        ("key_c", pa.float64()),
        ("key_d", pa.bool_()),
        ("key_e", pa.timestamp("s",  tz=utc)),
        ("key_f", pa.timestamp("ms", tz=utc)),
        ("key_g", pa.timestamp("ns", tz=utc)),
    ])
    ```

    Args:
        schema_template (Sequence[Sequence[str]]): Data names and parquet types for creating the schema.

    Returns:
        pa.schema: Final parquet schema.

    Raises:
        ValueError: If an unknown type name is encountered.
    """
    try:
        return pa.schema([(col, _get_pa_type(type_name)) for col, type_name in schema_template.items()])
    except KeyError as e:
        raise ValueError(f"Unknown type name: {e.args[0]!r}") from e


def force_dataframe_dtypes(
    dataframe: pd.DataFrame,
    template: dict[str, str],
) -> pd.DataFrame:
    """Force the data types of a dataframe using a template.

    Args:
        dataframe (pd.DataFrame): Dataframe to force types.
        template (dict[str, str]): Template to use for forcing types.

    Returns:
        pd.DataFrame: Dataframe with forced types.

    Raises:
        ValueError: If an unknown type name is encountered.
    """
    dtype = {}
    for col_name, col_type in template.items():
        if col_type == "string":
            dtype[col_name] = str
        elif col_type == "integer":
            dtype[col_name] = int
        elif col_type == "float":
            dtype[col_name] = float
        elif col_type == "bool":
            dtype[col_name] = bool
        elif col_type == "timestamp[s]":
            dataframe[col_name] = pd.to_datetime(dataframe[col_name], unit="s", utc=True)
        elif col_type == "timestamp[ms]":
            dataframe[col_name] = pd.to_datetime(dataframe[col_name], unit="ms", utc=True)
        elif col_type == "timestamp[ns]":
            dataframe[col_name] = pd.to_datetime(dataframe[col_name], unit="ns", utc=True)
        else:
            raise ValueError(f"Unknown type name: {col_type!r}")
    return dataframe.astype(dtype=dtype)


def export_dataset(
    data: list[dict] | deque[dict] | pd.DataFrame,
    output_location: str | FilePath,
    primary_template: dict[str, str],
    partitions_template: dict[str, str],
    *,
    basename_template: str | None = None,
    use_s3: bool = False,
    use_threads: bool = False,
    overwrite: bool = False,
    boto3_client_kwargs: dict[str, Any] | None = None,
) -> None:
    """Write to dataset to local filesystem or AWS S3.

    Args:
        data (list[dict] | deque[dict] | pd.DataFrame]): List, deque, or dataframe of objects to be written.
        output_location (str | FilePath): Location to write the dataset to.
        primary_template (dict[str, str]): Parquet schema template to use for the table (excluding partitions).
        partitions_template(dict[str, str]): Parquet schema template to use for the partitions.
        basename_template (str, optional): Filename template to use when writing to S3 or locally. Defaults to None.
        use_s3 (bool, optional): Use S3 as the destination when exporting parquet files. Defaults to False.
        use_threads (bool, optional): Use multiple threads when exporting. Defaults to False.
        overwrite (bool, optional): Overwrite existing files. Defaults to False.
        boto3_client_kwargs (dict[str, Any], optional): Keyword arguments to use when constructing the boto3 client. Defaults to None.
    """
    if isinstance(data, pd.DataFrame):
        # Already a dataframe
        dataframe = data
    elif isinstance(data, deque):
        # Create from deque
        dataframe = pd.DataFrame(list(data))
    else:
        # Create from list
        dataframe = pd.DataFrame(data)
    dataframe = force_dataframe_dtypes(
        dataframe,
        primary_template | partitions_template,
    )

    primary_schema = create_pa_schema(primary_template)
    partitions_schema = create_pa_schema(partitions_template)

    pa_table = pa.Table.from_pandas(
        dataframe,
        preserve_index=False,
        schema=primary_schema,
    )
    # logger.debug(f"Created Pyarrow table\n{pa_table!r}")

    if use_s3:
        filesystem = s3fs.S3FileSystem(
            anon=False,
            key=boto3_client_kwargs.get("aws_access_key_id"),
            secret=boto3_client_kwargs.get("aws_secret_access_key"),
            token=boto3_client_kwargs.get("aws_session_token"),
            client_kwargs={
                k: v
                for k, v in boto3_client_kwargs.items()
                if k not in ("aws_access_key_id", "aws_secret_access_key", "aws_session_token")
            },
        )
    else:
        # Stringify path and ensure it is absolute
        output_location = stringify_path(output_location)

        # TODO: Raise error here if `boto3_session_kwargs` is not None?
        local = fs.LocalFileSystem()
        filesystem = ArrowFSWrapper(local)

    ds.write_dataset(
        pa_table,
        output_location,
        basename_template=basename_template,
        format=ds.ParquetFileFormat(),
        schema=primary_schema,
        # A template string used to generate basenames of written data files.
        #     The token ‘{i}’ will be replaced with an automatically incremented integer.
        #     If not specified, it defaults to “part-{i}.” + format.default_extname
        # basename_template=basename_template,
        #     If nothing passed, will be inferred from where if path-like, else where is already a file-like object so no filesystem is needed.
        filesystem=filesystem,
        partitioning=ds.partitioning(partitions_schema, flavor="hive"),
        # Whether to use the global CPU thread pool to parallelize any computational tasks like compression.
        use_threads=use_threads,
        # Maximum number of partitions any batch may be written into.
        max_partitions=2048,
        # Controls how the dataset will handle data that already exists in the destination.
        #     The default behavior ('error') is to raise an error if any data exists in the destination.
        #     'overwrite_or_ignore' will ignore any existing data and will overwrite files with the same name as an output file.
        #     Other existing files will be ignored.
        #     This behavior, in combination with a unique basename_template for each write, will allow for an append workflow.
        #     'delete_matching' is useful when you are writing a partitioned dataset.
        #     The first time each partition directory is encountered the entire directory will be deleted.
        #     This allows you to overwrite old partitions completely.
        existing_data_behavior="overwrite_or_ignore" if overwrite else "error",
    )
    # logger.info(f"Exported as Parquet file to {output_location}")
