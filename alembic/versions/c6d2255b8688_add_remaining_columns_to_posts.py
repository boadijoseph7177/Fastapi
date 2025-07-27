"""add remaining columns to posts

Revision ID: c6d2255b8688
Revises: 5efe461bcaf6
Create Date: 2025-07-12 01:31:22.550125

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6d2255b8688"
down_revision: Union[str, Sequence[str], None] = "5efe461bcaf6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", "posts", type_="foreignkey")
    op.drop_column("posts", "owner_id")
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    op.drop_column("posts", "content")
