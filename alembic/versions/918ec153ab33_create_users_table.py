"""create users table

Revision ID: 918ec153ab33
Revises: 72ced5ab6034
Create Date: 2022-07-27 14:39:56.065470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '918ec153ab33'
down_revision = '72ced5ab6034'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
