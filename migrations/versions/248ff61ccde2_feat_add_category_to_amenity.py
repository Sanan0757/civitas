"""feat: add category to amenity

Revision ID: 248ff61ccde2
Revises: 2c14bb9a4895
Create Date: 2025-02-17 14:53:35.009560

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "248ff61ccde2"
down_revision: Union[str, None] = "2c14bb9a4895"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "amenities", sa.Column("amenity_category", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("amenities", "amenity_category")
    # ### end Alembic commands ###
