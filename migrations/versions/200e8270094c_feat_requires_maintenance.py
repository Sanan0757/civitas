"""feat: requires_maintenance

Revision ID: 200e8270094c
Revises: 50fd789492b2
Create Date: 2025-02-14 17:03:20.402450

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "200e8270094c"
down_revision: Union[str, None] = "50fd789492b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "buildings",
        sa.Column(
            "requires_maintenance", sa.Boolean(), server_default="false", nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("buildings", "requires_maintenance")
    # ### end Alembic commands ###
