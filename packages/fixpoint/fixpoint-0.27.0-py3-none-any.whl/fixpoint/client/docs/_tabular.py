"""Code for making tabular documents."""

__all__ = ["TableRow", "TableContents"]

import json

from typing import Any, Dict, Iterable, List, Set, Tuple

from ..types import Document


TABULAR_MEDIA_TYPE = "application/json;fixpoint-format=tabular"


class TableRow:
    """
    Represents a single row in a table.

    Attributes:
        cells (Dict[str, Any]): A dictionary containing column names as keys and
            cell values as values.
    """

    cells: Dict[str, Any]

    def __init__(self, cells: Dict[str, Any]) -> None:
        """
        Initialize a TableRow instance.

        Args:
            cells (Dict[str, Any]): A dictionary of column names and cell values.
        """
        self.cells = cells

    def __repr__(self) -> str:
        inner = ", ".join(f"{k}={v}" for k, v in self.items())
        return f"TableRow({inner})"

    def items(self) -> Iterable[Tuple[str, Any]]:
        """
        Return an iterable of (column_name, cell_value) pairs.

        Returns:
            Iterable[Tuple[str, Any]]: An iterable of (column_name, cell_value) tuples.
        """
        return self.cells.items()

    def keys(self) -> Iterable[str]:
        """
        Return an iterable of column names.

        Returns:
            Iterable[str]: An iterable of column names.
        """
        return self.cells.keys()

    def values(self) -> Iterable[Any]:
        """
        Return an iterable of cell values.

        Returns:
            Iterable[Any]: An iterable of cell values.
        """
        return self.cells.values()


class TableContents:
    """
    A tabular data structure representing a table with columns and rows.

    Attributes:
        columns_keys (List[str]): A list of column names.
    """

    columns_keys: List[str]
    _col_key_set: Set[str]
    _rows: List[TableRow]

    def __init__(self, columns_keys: List[str]) -> None:
        """
        Initialize a TableContents instance.

        Args:
            columns_keys (List[str]): A list of column names for the table.
        """
        self.columns_keys = columns_keys
        self._rows = []
        self._col_key_set = set(columns_keys)

    def add_row(self, row: TableRow) -> None:
        """
        Add a row to the table.

        Args:
            row (TableRow): The row to be added to the table.

        Raises:
            ValueError: If the row keys do not match the table columns.
        """
        row_keys = set(row.keys())
        if row_keys != self._col_key_set:
            raise ValueError(
                "Row keys do not match table columns. "
                f"Expected {self._col_key_set}, got {row_keys}"
            )
        self._rows.append(row)

    def rows(self) -> Iterable[TableRow]:
        """
        Return an iterable of all rows in the table.

        Returns:
            Iterable[TableRow]: An iterable of TableRow objects.
        """
        return self._rows

    def to_json(self, *, indent: int | str | None = None) -> str:
        """
        Convert the table contents to a JSON string.

        Returns:
            str: A JSON string representation of the table.
        """
        return json.dumps(self._to_list_table(), indent=indent)

    def to_json_document(
        self, doc_template: Document, *, indent: int | str | None = None
    ) -> Document:
        """
        Convert the table contents to a JSON-based Document object.

        Args:
            doc_template (Document): A template Document object to use as a base.

        Returns:
            Document: A new Document object with the table contents and updated media type.
        """
        doc_copy = doc_template.model_copy()
        doc_copy.contents = self.to_json(indent=indent)
        doc_copy.media_type = TABULAR_MEDIA_TYPE
        return doc_copy

    def _to_list_table(self) -> List[Dict[str, Any]]:
        """
        Convert the table contents to a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the table rows.
        """
        return [row.cells.copy() for row in self._rows]
