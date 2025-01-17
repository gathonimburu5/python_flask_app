"""create users

Revision ID: e43415a0feda
Revises: 3da0a95fe0fb
Create Date: 2024-10-29 14:29:16.565811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e43415a0feda'
down_revision = '3da0a95fe0fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Fullnames', sa.String(length=100), nullable=False),
    sa.Column('Email', sa.String(length=255), nullable=False),
    sa.Column('Phone', sa.String(length=14), nullable=False),
    sa.Column('PostalAddress', sa.String(length=100), nullable=False),
    sa.Column('PhysicalAddress', sa.String(length=200), nullable=False),
    sa.Column('County', sa.String(length=50), nullable=False),
    sa.Column('DOB', sa.DateTime(), nullable=False),
    sa.Column('Username', sa.String(length=255), nullable=False),
    sa.Column('Password', sa.String(length=255), nullable=False),
    sa.Column('ProfilePic', sa.String(length=255), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Id'),
    sa.UniqueConstraint('Email'),
    sa.UniqueConstraint('Username')
    )
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('Author',
               existing_type=sa.VARCHAR(length=100),
               nullable=100)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('Author',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    op.drop_table('users')
    # ### end Alembic commands ###
