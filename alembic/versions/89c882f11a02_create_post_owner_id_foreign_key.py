"""create post owner id foreign key

Revision ID: 89c882f11a02
Revises: 918ec153ab33
Create Date: 2022-07-27 16:21:21.685549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c882f11a02'
down_revision = '918ec153ab33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa. Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts', 'owner_id')
