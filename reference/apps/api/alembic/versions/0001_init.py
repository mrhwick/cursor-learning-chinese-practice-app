"""init

Revision ID: 0001_init
Revises: 
Create Date: 2026-02-07

"""

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "classrooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("invite_code", sa.String(length=32), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_classrooms_invite_code"), "classrooms", ["invite_code"], unique=True)

    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("classroom_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["classroom_id"], ["classrooms.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "classroom_id", name="uq_enrollment_user_classroom"),
    )
    op.create_index(op.f("ix_enrollments_classroom_id"), "enrollments", ["classroom_id"], unique=False)
    op.create_index(op.f("ix_enrollments_user_id"), "enrollments", ["user_id"], unique=False)

    op.create_table(
        "phrases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("classroom_id", sa.Integer(), nullable=False),
        sa.Column("chinese", sa.String(length=500), nullable=False),
        sa.Column("pinyin", sa.String(length=500), nullable=False),
        sa.Column("english", sa.String(length=500), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["classroom_id"], ["classrooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_phrases_classroom_id"), "phrases", ["classroom_id"], unique=False)

    op.create_table(
        "model_audio",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phrase_id", sa.Integer(), nullable=False),
        sa.Column("storage_path", sa.String(length=500), nullable=False),
        sa.Column("original_filename", sa.String(length=500), nullable=False),
        sa.Column("content_type", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["phrase_id"], ["phrases.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phrase_id"),
    )
    op.create_index(op.f("ix_model_audio_phrase_id"), "model_audio", ["phrase_id"], unique=False)

    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phrase_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("storage_path", sa.String(length=500), nullable=False),
        sa.Column("original_filename", sa.String(length=500), nullable=False),
        sa.Column("content_type", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["phrase_id"], ["phrases.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_submissions_phrase_id"), "submissions", ["phrase_id"], unique=False)
    op.create_index(op.f("ix_submissions_user_id"), "submissions", ["user_id"], unique=False)

    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("score_tones", sa.Integer(), nullable=False),
        sa.Column("score_clarity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["submission_id"], ["submissions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_feedback_author_id"), "feedback", ["author_id"], unique=False)
    op.create_index(op.f("ix_feedback_submission_id"), "feedback", ["submission_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_feedback_submission_id"), table_name="feedback")
    op.drop_index(op.f("ix_feedback_author_id"), table_name="feedback")
    op.drop_table("feedback")

    op.drop_index(op.f("ix_submissions_user_id"), table_name="submissions")
    op.drop_index(op.f("ix_submissions_phrase_id"), table_name="submissions")
    op.drop_table("submissions")

    op.drop_index(op.f("ix_model_audio_phrase_id"), table_name="model_audio")
    op.drop_table("model_audio")

    op.drop_index(op.f("ix_phrases_classroom_id"), table_name="phrases")
    op.drop_table("phrases")

    op.drop_index(op.f("ix_enrollments_user_id"), table_name="enrollments")
    op.drop_index(op.f("ix_enrollments_classroom_id"), table_name="enrollments")
    op.drop_table("enrollments")

    op.drop_index(op.f("ix_classrooms_invite_code"), table_name="classrooms")
    op.drop_table("classrooms")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

