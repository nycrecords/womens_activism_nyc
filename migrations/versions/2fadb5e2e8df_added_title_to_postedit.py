"""added title to PostEdit

Revision ID: 2fadb5e2e8df
Revises: 8f5389a952dd
Create Date: 2016-08-05 14:26:22.786417

"""

# revision identifiers, used by Alembic.
revision = '2fadb5e2e8df'
down_revision = '8f5389a952dd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_edits', sa.Column('title', sa.String(length=140), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post_edits', 'title')
    ### end Alembic commands ###