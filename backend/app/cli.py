"""Administrative bootstrap commands; never expose account creation publicly."""

import argparse
import getpass
import sys

from sqlalchemy import func, select

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password


def create_user(email: str, role: str) -> None:
    normalized_email = email.strip().lower()
    if role not in {"admin", "admission_staff", "student"}:
        raise SystemExit("Role must be admin, admission_staff, or student.")
    password = getpass.getpass("New password (minimum 12 characters): ")
    confirmation = getpass.getpass("Confirm password: ")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")
    try:
        password_hash = hash_password(password)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    with SessionLocal() as db:
        existing = db.scalar(select(User.id).where(func.lower(User.email) == normalized_email))
        if existing is not None:
            raise SystemExit("A user with that email already exists.")
        if role == "student":
            raise SystemExit(
                "Student accounts must be provisioned through a verified student-linking workflow; "
                "this command does not create unlinked student accounts."
            )
        db.add(User(email=normalized_email, password_hash=password_hash, role=role, is_active=True))
        db.commit()
    print(f"Created {role} account for {normalized_email}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="College ERP account administration")
    subparsers = parser.add_subparsers(dest="command", required=True)
    create_parser = subparsers.add_parser("create-user", help="Create an admin or admission staff account")
    create_parser.add_argument("--email", required=True)
    create_parser.add_argument("--role", required=True, choices=["admin", "admission_staff"])
    args = parser.parse_args()
    try:
        create_user(args.email, args.role)
    except Exception as exc:
        print(f"Could not create account: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
