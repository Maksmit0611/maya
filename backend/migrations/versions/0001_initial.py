"""Initial MAYA project, room, brief, job, and result schema."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None
JSON_TYPE = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")
UUID_TYPE = sa.Uuid(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column("owner_id", sa.String(128), nullable=False, index=True),
        sa.Column("name", sa.String(180), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "project_members",
        sa.Column(
            "project_id",
            UUID_TYPE,
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("user_id", sa.String(128), primary_key=True),
        sa.Column("role", sa.String(24), nullable=False, server_default="member"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_project_members_user_id", "project_members", ["user_id"])
    op.create_table(
        "rooms",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column(
            "project_id",
            UUID_TYPE,
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("name", sa.String(180), nullable=False),
        sa.Column("room_type", sa.String(80), nullable=False, server_default="living room"),
        sa.Column("dimensions", JSON_TYPE, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "assets",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column(
            "project_id",
            UUID_TYPE,
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "room_id",
            UUID_TYPE,
            sa.ForeignKey("rooms.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        ),
        sa.Column("owner_id", sa.String(128), nullable=False),
        sa.Column("storage_path", sa.String(500), nullable=False, unique=True),
        sa.Column("mime_type", sa.String(120), nullable=False),
        sa.Column("kind", sa.String(40), nullable=False, server_default="image"),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "briefs",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column(
            "project_id",
            UUID_TYPE,
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "room_id", UUID_TYPE, sa.ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("content", JSON_TYPE, nullable=False),
        sa.Column("created_by", sa.String(128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_briefs_room_id", "briefs", ["room_id"])
    op.create_table(
        "agent_messages",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column(
            "project_id",
            UUID_TYPE,
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("user_id", sa.String(128), nullable=False),
        sa.Column("role", sa.String(24), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("structured", JSON_TYPE, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "generation_jobs",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column(
            "project_id",
            UUID_TYPE,
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "room_id", UUID_TYPE, sa.ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("requested_by", sa.String(128), nullable=False),
        sa.Column("job_type", sa.String(40), nullable=False, server_default="design"),
        sa.Column("status", sa.String(24), nullable=False, server_default="queued"),
        sa.Column("idempotency_key", sa.String(200), nullable=False),
        sa.Column("input_json", JSON_TYPE, nullable=False),
        sa.Column("provenance", JSON_TYPE, nullable=False, server_default="{}"),
        sa.Column(
            "cancellation_requested", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_json", JSON_TYPE, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "project_id", "idempotency_key", name="uq_generation_project_idempotency"
        ),
        sa.CheckConstraint(
            "status in ('queued','running','succeeded','failed','cancelled')",
            name="ck_generation_job_status",
        ),
    )
    op.create_index("ix_generation_jobs_room_id", "generation_jobs", ["room_id"])
    op.create_index(
        "ix_generation_jobs_queued_created_at",
        "generation_jobs",
        ["created_at"],
        postgresql_where=sa.text("status = 'queued'"),
        sqlite_where=sa.text("status = 'queued'"),
    )
    op.create_table(
        "results",
        sa.Column("id", UUID_TYPE, primary_key=True),
        sa.Column(
            "job_id",
            UUID_TYPE,
            sa.ForeignKey("generation_jobs.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "asset_id", UUID_TYPE, sa.ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("prompt_version", sa.String(40), nullable=False),
        sa.Column("prompt_hash", sa.String(64), nullable=False),
        sa.Column("seed", sa.BigInteger(), nullable=True),
        sa.Column("output_json", JSON_TYPE, nullable=False),
        sa.Column("selected_by", sa.String(128), nullable=True),
        sa.Column("selected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_results_asset_id", "results", ["asset_id"])


def downgrade() -> None:
    for table in (
        "results",
        "generation_jobs",
        "agent_messages",
        "briefs",
        "assets",
        "rooms",
        "project_members",
        "projects",
    ):
        op.drop_table(table)
