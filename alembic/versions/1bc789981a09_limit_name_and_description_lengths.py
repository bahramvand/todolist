"""limit name and description lengths

Revision ID: 1bc789981a09
Revises: 597cb975a847
Create Date: 2025-12-05 21:50:13.774624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from todolist.core.constants import (
    TASK_TITLE_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    TASK_DESCRIPTION_MAX_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
)

# revision identifiers, used by Alembic.
revision: str = '1bc789981a09'
down_revision: Union[str, Sequence[str], None] = '597cb975a847'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("projects", "name", type_=sa.String(length=PROJECT_NAME_MAX_LENGTH))
    op.alter_column("projects", "description", type_=sa.String(length=PROJECT_DESCRIPTION_MAX_LENGTH))

    op.alter_column("tasks", "title", type_=sa.String(length=TASK_TITLE_MAX_LENGTH))
    op.alter_column("tasks", "description", type_=sa.String(length=TASK_DESCRIPTION_MAX_LENGTH))


def downgrade() -> None:
    op.alter_column("projects", "name", type_=sa.String(length=255))
    op.alter_column("projects", "description", type_=sa.Text())

    op.alter_column("tasks", "title", type_=sa.String(length=255))
    op.alter_column("tasks", "description", type_=sa.Text())