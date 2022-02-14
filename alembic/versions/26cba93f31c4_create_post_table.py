"""create post table

Revision ID: 26cba93f31c4
Revises: 
Create Date: 2022-02-03 20:35:48.308042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26cba93f31c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('phone', sa.String(), nullable=False, server_default="00000"))
    pass


def downgrade():
    op.drop_column('posts', 'phone')
    pass
