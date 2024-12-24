"""Postgres data types."""

from typing import TypedDict

import sqlalchemy.dialects.postgresql as sa_pg
import sqlalchemy.types as types
from sqlalchemy_utils import Ltree as PGLtree


__all__ = ['CITEXT', 'Ltree', 'MigrationState']


class MigrationState(TypedDict):
    """Migration service migration.

    This data format is used by migration services to perform migrations. See an example below.

    .. code-block:: python

        {
            "id": 0,
            "comments": "dev comments",
            "commands": [
                "ALTER TABLE my_table ADD COLUMN new_col DEFAULT NULL;",
                "ALTER TABLE my_table DROP COLUMN old_col;",
            ]
        }

    """

    id: int  #: state id, sequential integer >= 0
    comments: str  #: human readable comments
    commands: list[str]  #: a list of sql commands performed inside a transaction block


class CITEXT(types.UserDefinedType, sa_pg.TEXT):
    """Postgres case-insensitive text data type."""

    def get_col_spec(self):  # noqa: required
        return 'CITEXT'


class Ltree(PGLtree):
    """Postgresql Ltree data type."""

    @classmethod
    def validate(cls, path):
        pass
