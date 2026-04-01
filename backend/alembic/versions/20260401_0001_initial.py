"""initial schema"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260401_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )
    op.create_unique_constraint("uq_topics_slug", "topics", ["slug"])
    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("daily_schedule_time", sa.Time(), nullable=False),
        sa.Column("briefing_length_minutes", sa.Integer(), nullable=False),
        sa.Column("include_weekends", sa.Boolean(), nullable=False),
    )
    op.create_unique_constraint("uq_user_settings_user_id", "user_settings", ["user_id"])
    op.create_table(
        "user_topic_preferences",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("topics.id"), nullable=False),
        sa.Column("priority_weight", sa.Float(), nullable=False),
    )
    op.create_unique_constraint("uq_user_topic", "user_topic_preferences", ["user_id", "topic_id"])
    op.create_table(
        "source_articles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_name", sa.String(length=120), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("topic_slug", sa.String(length=64), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=False),
        sa.Column("credibility_score", sa.Float(), nullable=False),
        sa.Column("importance_score", sa.Float(), nullable=False),
        sa.Column("normalized_hash", sa.String(length=128), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint("uq_source_articles_url", "source_articles", ["url"])
    op.create_index("ix_source_articles_normalized_hash", "source_articles", ["normalized_hash"], unique=False)
    op.create_table(
        "news_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cluster_key", sa.String(length=128), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("topic_slug", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("why_it_matters", sa.Text(), nullable=False),
        sa.Column("source_count", sa.Integer(), nullable=False),
        sa.Column("global_importance", sa.Float(), nullable=False),
        sa.Column("recency_score", sa.Float(), nullable=False),
        sa.Column("novelty_score", sa.Float(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_news_events_cluster_key", "news_events", ["cluster_key"], unique=True)
    op.create_table(
        "briefings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("script", sa.Text(), nullable=False),
        sa.Column("audio_path", sa.String(length=500), nullable=True),
        sa.Column("status", sa.Enum("pending", "ready", "failed", name="briefingstatus"), nullable=False),
        sa.Column("generation_mode", sa.String(length=32), nullable=False),
        sa.Column("generated_at", sa.DateTime(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    )
    op.create_index("ix_briefings_generated_at", "briefings", ["generated_at"], unique=False)
    op.create_table(
        "briefing_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("briefing_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("briefings.id"), nullable=False),
        sa.Column("event_title", sa.Text(), nullable=False),
        sa.Column("section", sa.String(length=64), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("why_it_matters", sa.Text(), nullable=False),
        sa.Column("topic_slug", sa.String(length=64), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("article_urls", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    )
    op.create_table(
        "voice_profiles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("provider_status", sa.Enum("standard", "cloning_pending", "custom_ready", "unavailable", name="voiceproviderstatus"), nullable=False),
        sa.Column("sample_path", sa.String(length=500), nullable=True),
        sa.Column("provider_voice_id", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("voice_profiles")
    op.drop_table("briefing_items")
    op.drop_index("ix_briefings_generated_at", table_name="briefings")
    op.drop_table("briefings")
    op.drop_index("ix_news_events_cluster_key", table_name="news_events")
    op.drop_table("news_events")
    op.drop_index("ix_source_articles_normalized_hash", table_name="source_articles")
    op.drop_table("source_articles")
    op.drop_table("user_topic_preferences")
    op.drop_table("user_settings")
    op.drop_constraint("uq_topics_slug", "topics", type_="unique")
    op.drop_table("topics")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS voiceproviderstatus")
    op.execute("DROP TYPE IF EXISTS briefingstatus")
