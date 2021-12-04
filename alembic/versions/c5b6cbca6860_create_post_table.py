"""create post Table

Revision ID: c5b6cbca6860
Revises: 
Create Date: 2021-12-04 11:08:29.994335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5b6cbca6860'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
     op.create_table('posts_alembic', 
     sa.Column('id', sa.Integer(), nullable=False,primary_key=True), sa.Column('title', sa.String(), nullable=False),
     sa.Column('title', sa.String(), nullable=False),
     sa.Column('content', sa.String(), nullable=False),
     sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
     sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )
    


def downgrade():
    op.drop_table('posts')
