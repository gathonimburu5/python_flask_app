"""empty message

Revision ID: 3da0a95fe0fb
Revises: 
Create Date: 2024-09-21 10:43:23.473624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3da0a95fe0fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Code', sa.String(length=100), nullable=False),
    sa.Column('Name', sa.String(length=200), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Id'),
    sa.UniqueConstraint('Code')
    )
    op.create_table('book',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Tittle', sa.String(length=100), nullable=False),
    sa.Column('Author', sa.String(length=100), nullable=100),
    sa.Column('ISBN', sa.String(length=30), nullable=False),
    sa.Column('PublishedOn', sa.DateTime(), nullable=False),
    sa.Column('CourseId', sa.Integer(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['CourseId'], ['course.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('student',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('AdmNo', sa.String(length=50), nullable=False),
    sa.Column('FullNames', sa.String(length=100), nullable=False),
    sa.Column('EmailAddress', sa.String(length=255), nullable=True),
    sa.Column('PhoneNumber', sa.String(length=15), nullable=False),
    sa.Column('County', sa.String(length=100), nullable=False),
    sa.Column('CourseId', sa.Integer(), nullable=True),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['CourseId'], ['course.Id'], ),
    sa.PrimaryKeyConstraint('Id'),
    sa.UniqueConstraint('AdmNo'),
    sa.UniqueConstraint('EmailAddress')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    op.drop_table('book')
    op.drop_table('course')
    # ### end Alembic commands ###
