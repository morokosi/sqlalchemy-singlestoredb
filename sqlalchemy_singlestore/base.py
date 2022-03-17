#!/usr/bin/env python
"""Base classes for SingleStore SQLAlchemy objects."""
from __future__ import annotations

from typing import Any
from typing import List
from typing import Type

from singlestore.connection import build_params
from sqlalchemy import util
from sqlalchemy.dialects.mysql.base import BIT  # noqa: F401
from sqlalchemy.dialects.mysql.base import MySQLCompiler
from sqlalchemy.dialects.mysql.base import MySQLDDLCompiler
from sqlalchemy.dialects.mysql.base import MySQLDialect
from sqlalchemy.dialects.mysql.base import MySQLExecutionContext
from sqlalchemy.dialects.mysql.base import MySQLIdentifierPreparer
from sqlalchemy.dialects.mysql.base import MySQLTypeCompiler
from sqlalchemy.dialects.mysql.base import TEXT  # noqa: F401
from sqlalchemy.engine.url import URL

from . import reflection


class SingleStoreExecutionContext(MySQLExecutionContext):
    """SingleStore SQLAlchemy execution context."""


class SingleStoreCompiler(MySQLCompiler):
    """SingleStore SQLAlchemy compiler."""


class SingleStoreDDLCompiler(MySQLDDLCompiler):
    """SingleStore SQLAlchemy DDL compiler."""


class SingleStoreTypeCompiler(MySQLTypeCompiler):
    """SingleStore SQLAlchemy type compiler."""


class SingleStoreIdentifierPreparer(MySQLIdentifierPreparer):
    """SingleStore SQLAlchemy identifier preparer."""


class SingleStoreDialect(MySQLDialect):
    """SingleStore SQLAlchemy dialect."""

    name = 'singlestore'

    default_paramstyle = 'named'

    statement_compiler = SingleStoreCompiler
    ddl_compiler = SingleStoreDDLCompiler
    type_compiler = SingleStoreTypeCompiler
    preparer = SingleStoreIdentifierPreparer

    @classmethod
    def dbapi(cls) -> Any:
        return __import__('singlestore')

    def create_connect_args(self, url: URL) -> List[Any]:
        return [[], build_params(host=str(url))]

    def _extract_error_code(self, exception: Exception) -> int:
        return getattr(exception, 'errno', -1)

    def _detect_charset(self, connection: Any) -> str:
        return 'utf8mb4'

    @util.memoized_property
    def _tabledef_parser(self) -> reflection.SingleStoreTableDefinitionParser:
        """
        Return the SingleStoreTableDefinitionParser.

        The deferred creation ensures that the dialect has
        retrieved server version information first.

        Returns
        -------
        reflection.SingleStoreTableDefinitionParser

        """
        from . import reflection
        preparer = self.identifier_preparer
        return reflection.SingleStoreTableDefinitionParser(self, preparer)


dialect: Type[SingleStoreDialect] = SingleStoreDialect
