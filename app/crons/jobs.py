from .scheduler import scheduler

def sync_users():
    print("syncing users...")

scheduler.add_job(
    sync_users,
    trigger="cron",
    minute="*",
    id="sync_users"
)

