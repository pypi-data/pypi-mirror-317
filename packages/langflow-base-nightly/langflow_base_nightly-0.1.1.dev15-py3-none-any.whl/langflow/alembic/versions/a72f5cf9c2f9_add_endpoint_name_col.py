"""Add endpoint name col

Revision ID: a72f5cf9c2f9
Revises: 29fe8f1f806b
Create Date: 2024-05-29 21:44:04.240816

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "a72f5cf9c2f9"
down_revision: Union[str, None] = "29fe8f1f806b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)  # type: ignore
    # ### commands auto generated by Alembic - please adjust! ###
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    indexes = inspector.get_indexes("flow")
    index_names = [index["name"] for index in indexes]
    with op.batch_alter_table("flow", schema=None) as batch_op:
        if "endpoint_name" not in column_names:
            batch_op.add_column(sa.Column("endpoint_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        if "ix_flow_endpoint_name" not in index_names:
            batch_op.create_index(batch_op.f("ix_flow_endpoint_name"), ["endpoint_name"], unique=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)  # type: ignore
    # ### commands auto generated by Alembic - please adjust! ###
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    indexes = inspector.get_indexes("flow")
    index_names = [index["name"] for index in indexes]
    with op.batch_alter_table("flow", schema=None) as batch_op:
        if "ix_flow_endpoint_name" in index_names:
            batch_op.drop_index(batch_op.f("ix_flow_endpoint_name"))
        if "endpoint_name" in column_names:
            batch_op.drop_column("endpoint_name")

    # ### end Alembic commands ###
