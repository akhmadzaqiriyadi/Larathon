"""
Migration: create_users_and_related_tables
"""
from sqlalchemy import (Table, Column, Integer, String, MetaData, TIMESTAMP,
                        ForeignKey, Text, text) # <-- Perbaikan di sini
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

def up(engine):
    meta = MetaData()

    # Enable pgcrypto extension for UUID generation
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\""))
        conn.commit()

    # 1. Tabel Users
    users = Table(
        "users", meta,
        Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
        Column("email", Text, unique=True, nullable=False, index=True),
        Column("username", Text, unique=True, nullable=False, index=True),
        Column("password_hash", Text, nullable=False),
        Column("created_at", TIMESTAMP(timezone=True), default=datetime.utcnow),
        Column("updated_at", TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # 2. Tabel User Profiles
    user_profiles = Table(
        "user_profiles", meta,
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        Column("full_name", Text),
        Column("bio", Text),
        Column("avatar_url", Text),
        Column("created_at", TIMESTAMP(timezone=True), default=datetime.utcnow),
        Column("updated_at", TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # 3. Tabel Roles
    roles = Table(
        "roles", meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", Text, unique=True, nullable=False),
        Column("description", Text)
    )

    # 4. Tabel User Roles (Junction Table)
    user_roles = Table(
        "user_roles", meta,
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    )

    # 5. Tabel Divisions
    divisions = Table(
        "divisions", meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", Text, unique=True, nullable=False),
        Column("description", Text)
    )

    # 6. Tabel User Divisions (Junction Table)
    user_divisions = Table(
        "user_divisions", meta,
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        Column("division_id", Integer, ForeignKey("divisions.id", ondelete="CASCADE"), primary_key=True)
    )

    meta.create_all(engine)
    print("🔼 Creating users, profiles, roles, and divisions tables.")

def down(engine):
    meta = MetaData()
    meta.reflect(bind=engine)

    # Hapus tabel dalam urutan yang benar (dari yang paling ketergantungan)
    meta.tables['user_divisions'].drop(engine)
    meta.tables['user_roles'].drop(engine)
    meta.tables['divisions'].drop(engine)
    meta.tables['roles'].drop(engine)
    meta.tables['user_profiles'].drop(engine)
    meta.tables['users'].drop(engine)

    print("🔽 Dropping all authentication tables.")
