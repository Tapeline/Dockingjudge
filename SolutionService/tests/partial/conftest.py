import os
import sqlite3
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from solution_service.infrastructure.persistence.repo_impl import (
    SolutionRepoImpl,
)


@pytest.fixture
def sqlite_base():
    conn = sqlite3.connect("test_base.db")
    use_solution_table(conn)
    conn.close()
    yield "test_base.db"
    try:
        os.remove("test_base.db")
    except PermissionError:
        conn = sqlite3.connect("test_base.db")
        clean_solution_table(conn)
        conn.close()


def use_solution_table(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS solutions (
            uuid TEXT PRIMARY KEY NOT NULL,
            contest_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            task_type TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            short_verdict TEXT NOT NULL,
            answer TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            code_solution_type TEXT NULL,
            compiler_name TEXT NULL,
            group_scores TEXT NULL,
            detailed_verdict TEXT NULL,
            main_file TEXT NULL
        );
        """,
    )
    conn.commit()


def clean_solution_table(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        DROP TABLE IF EXISTS solutions;
        """,
    )
    conn.commit()


@pytest_asyncio.fixture
async def solution_repo(
    sqlite_base: str,
) -> AsyncGenerator[SolutionRepoImpl, Any]:
    engine = create_async_engine(
        f"sqlite+aiosqlite:///./{sqlite_base}",
    )
    async_session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession,
    )
    async with async_session_maker() as session:
        yield SolutionRepoImpl(session)
