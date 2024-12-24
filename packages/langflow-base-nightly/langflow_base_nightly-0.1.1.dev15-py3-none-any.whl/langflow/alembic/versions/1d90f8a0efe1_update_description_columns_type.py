"""Update description columns type

Revision ID: 4522eb831f5c
Revises: 0d60fcbd4e8e
Create Date: 2024-08-20 11:46:56.266061

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

from langflow.utils import migration

# revision identifiers, used by Alembic.
revision: str = "4522eb831f5c"
down_revision: Union[str, None] = "0d60fcbd4e8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    inspector = sa.inspect(conn)  # type: ignore

    with op.batch_alter_table("flow", schema=None) as batch_op:
        if migration.column_exists(table_name="flow", column_name="description", conn=conn):
            columns = inspector.get_columns("flow")
            description_column = next((column for column in columns if column["name"] == "description"), None)
            if description_column is not None and isinstance(description_column["type"], sa.VARCHAR):
                batch_op.alter_column(
                    "description", existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
                )

    with op.batch_alter_table("folder", schema=None) as batch_op:
        if migration.column_exists(table_name="folder", column_name="description", conn=conn):
            columns = inspector.get_columns("folder")
            description_column = next((column for column in columns if column["name"] == "description"), None)
            if description_column is not None and isinstance(description_column["type"], sa.VARCHAR):
                batch_op.alter_column(
                    "description", existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
                )

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    inspector = sa.inspect(conn)  # type: ignore
    with op.batch_alter_table("folder", schema=None) as batch_op:
        if migration.column_exists(table_name="folder", column_name="description", conn=conn):
            columns = inspector.get_columns("folder")
            description_column = next((column for column in columns if column["name"] == "description"), None)
            if description_column is not None and isinstance(description_column["type"], sa.VARCHAR):
                batch_op.alter_column(
                    "description", existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
                )

    with op.batch_alter_table("flow", schema=None) as batch_op:
        if migration.column_exists(table_name="flow", column_name="description", conn=conn):
            columns = inspector.get_columns("flow")
            description_column = next((column for column in columns if column["name"] == "description"), None)
            if description_column is not None and isinstance(description_column["type"], sa.VARCHAR):
                batch_op.alter_column(
                    "description", existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
                )
    # ### end Alembic commands ###
