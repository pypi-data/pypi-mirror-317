"""Add webhook columns

Revision ID: 631faacf5da2
Revises: 1c79524817ed
Create Date: 2024-04-22 15:14:43.454784

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "631faacf5da2"
down_revision: Union[str, None] = "1c79524817ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)  # type: ignore
    table_names = inspector.get_table_names()
    # ### commands auto generated by Alembic - please adjust! ###
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    with op.batch_alter_table("flow", schema=None) as batch_op:
        if "flow" in table_names and "webhook" not in column_names:
            batch_op.add_column(sa.Column("webhook", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)  # type: ignore
    table_names = inspector.get_table_names()
    # ### commands auto generated by Alembic - please adjust! ###
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    with op.batch_alter_table("flow", schema=None) as batch_op:
        if "flow" in table_names and "webhook" in column_names:
            batch_op.drop_column("webhook")

    # ### end Alembic commands ###
