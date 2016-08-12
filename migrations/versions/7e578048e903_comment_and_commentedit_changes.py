"""Comment and CommentEdit changes

Revision ID: 7e578048e903
Revises: 2cdfa5e0b5c5
Create Date: 2016-08-12 10:56:36.559340

"""

# revision identifiers, used by Alembic.
revision = '7e578048e903'
down_revision = '2cdfa5e0b5c5'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment_edits', sa.Column('creation_time', sa.DateTime(), nullable=True))
    op.add_column('comment_edits', sa.Column('version', sa.Integer(), nullable=True))
    op.alter_column('comment_edits', 'edit_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.add_column('comments', sa.Column('edit_time', sa.DateTime(), nullable=True))
    op.add_column('comments', sa.Column('version', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'version')
    op.drop_column('comments', 'edit_time')
    op.alter_column('comment_edits', 'edit_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('comment_edits', 'version')
    op.drop_column('comment_edits', 'creation_time')
    ### end Alembic commands ###