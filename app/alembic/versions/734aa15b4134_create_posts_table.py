"""create posts table

Revision ID: 734aa15b4134
Revises: 
Create Date: 2022-10-23 18:33:05.347415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '734aa15b4134'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
