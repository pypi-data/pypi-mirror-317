# -*- coding: utf-8 -*-

import csv

from io import StringIO
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List


def records_from_csv(
        path: str, file_args: Dict = None,
        reader_args: Dict = None) -> Iterator[Dict]:

    """ Returns records from a CSV file """

    file_args = file_args or {}
    reader_args = reader_args or {}

    with open(path, **file_args) as f_:
        reader = csv.DictReader(f_, **reader_args)
        for rec in reader:
            yield rec


def records_from_buffer(
        data: str, newline: str = None, **kwargs) -> Iterator[Dict]:

    """ Returns records from file-like object """

    dialect = kwargs.pop("dialect", "excel")
    quoting = kwargs.pop("quoting", csv.QUOTE_NONNUMERIC)

    reader = csv.DictReader(
        StringIO(data, newline=newline),
        dialect=dialect, quoting=quoting,
        **kwargs)

    for rec in reader:
        yield rec


def records_to_buffer(
        records: List[Dict], columns: List[str] = None,
        **kwargs) -> StringIO:

    """ Save records from file-like object """

    buffer = StringIO()
    dialect = kwargs.pop("dialect", "excel")
    quoting = kwargs.pop("quoting", csv.QUOTE_NONNUMERIC)
    columns = columns or records[0].keys()

    csv_writer = csv.DictWriter(
        buffer, fieldnames=columns,
        dialect=dialect, quoting=quoting,
        **kwargs)

    csv_writer.writeheader()
    csv_writer.writerows(records)
    return buffer


def records_to_csv(
        file_path: str, records: Iterable[Dict], columns: List[str],
        quoting: int = csv.QUOTE_ALL, dialect=csv.excel, file_args: Dict = None,
        writer_args: Dict = None) -> None:

    file_args = file_args or {}
    writer_args = writer_args or {}

    with open(file_path, mode="w", **file_args) as file:
        writer = csv.DictWriter(
            file, fieldnames=columns, dialect=dialect,
            quoting=quoting, **writer_args)

        writer.writeheader()
        writer.writerows(records)
