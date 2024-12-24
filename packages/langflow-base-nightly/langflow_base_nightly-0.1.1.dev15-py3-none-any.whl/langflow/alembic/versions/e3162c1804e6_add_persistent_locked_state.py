"""add persistent locked state

Revision ID: e3162c1804e6
Revises: 1eab2c3eb45e
Create Date: 2024-11-07 14:50:35.201760

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'e3162c1804e6'
down_revision: Union[str, None] = '1eab2c3eb45e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flow', schema=None) as batch_op:
        if "locked" not in column_names:
            batch_op.add_column(sa.Column('locked', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flow', schema=None) as batch_op:
        if "locked" in column_names:
            batch_op.drop_column('locked')
    # ### end Alembic commands ###
