import argparse
import json
from datetime import datetime
from pathlib import Path

from psycopg2.extras import Json

import app


def parse_timestamp(value):
    if not value:
        return None
    text = str(value).strip().replace("T", " ").replace("Z", "")
    if "." in text:
        text = text.split(".", 1)[0]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return None


def import_users(users):
    for user_id, user in users.items():
        user = dict(user or {})
        user["id"] = user.get("id") or user.get("user_id") or user_id
        user["user_id"] = user["id"]
        if not user.get("account"):
            user["account"] = user["id"].lower()
        if not user.get("name"):
            user["name"] = user.get("account") or user["id"]
        app.upsert_user(user)


def import_logs(logs):
    with app.get_pg_conn() as conn:
        with conn.cursor() as cur:
            for log in logs:
                log = dict(log or {})
                created_at = parse_timestamp(log.get("timestamp") or log.get("created_at") or log.get("server_time"))
                if created_at:
                    cur.execute(
                        """
                        INSERT INTO behavior_logs (user_id, action_type, action_details, created_at)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (
                            log.get("user_id"),
                            log.get("action_type"),
                            Json(log.get("action_details") or log),
                            created_at,
                        ),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO behavior_logs (user_id, action_type, action_details)
                        VALUES (%s, %s, %s);
                        """,
                        (
                            log.get("user_id"),
                            log.get("action_type"),
                            Json(log.get("action_details") or log),
                        ),
                    )
        conn.commit()


def import_reflections(reflections):
    with app.get_pg_conn() as conn:
        with conn.cursor() as cur:
            for item in reflections:
                item = dict(item or {})
                reflection_date = app.normalize_date(item.get("reflection_date") or item.get("date"))
                created_at = parse_timestamp(item.get("created_at") or item.get("server_time") or item.get("submittedAt"))
                updated_at = parse_timestamp(item.get("updated_at") or item.get("updatedAt")) or created_at
                if created_at:
                    cur.execute(
                        """
                        INSERT INTO reflections
                            (user_id, reflection_id, reflection_date, reflection_data, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """,
                        (
                            item.get("user_id"),
                            item.get("reflection_id") or item.get("reflectionId"),
                            reflection_date,
                            Json(item),
                            created_at,
                            updated_at or created_at,
                        ),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO reflections (user_id, reflection_id, reflection_date, reflection_data)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (
                            item.get("user_id"),
                            item.get("reflection_id") or item.get("reflectionId"),
                            reflection_date,
                            Json(item),
                        ),
                    )
        conn.commit()


def clear_existing_data():
    with app.get_pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE behavior_logs, reflections RESTART IDENTITY;")
            cur.execute("DELETE FROM users;")
        conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Import legacy soulnav_db.json into PostgreSQL.")
    parser.add_argument("--file", default="soulnav_db.json", help="Path to legacy JSON database.")
    parser.add_argument("--replace", action="store_true", help="Clear current PostgreSQL data before importing.")
    args = parser.parse_args()

    source = Path(args.file)
    if not source.exists():
        raise FileNotFoundError(f"Cannot find {source}")

    app.initialize_database()
    data = json.loads(source.read_text(encoding="utf-8"))
    users = data.get("users", {})
    logs = data.get("logs", [])
    reflections = data.get("reflections", [])

    if args.replace:
        clear_existing_data()

    import_users(users)
    import_logs(logs)
    import_reflections(reflections)

    app.save_db()
    db = app.load_db()
    print("Legacy import complete.")
    print(f"Users: {len(db.get('users', {}))}")
    print(f"Behavior logs: {len(db.get('logs', []))}")
    print(f"Reflections: {len(db.get('reflections', []))}")


if __name__ == "__main__":
    main()
