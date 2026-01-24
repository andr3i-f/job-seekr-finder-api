import asyncio
from app.core.crons.scheduler import start_scheduler

# Needed to load crons before running scheduler
import app.core.crons.crons # noqa: F401

async def run_scheduler() -> None:
    start_scheduler()
    await asyncio.Event().wait()

def main():
    asyncio.run(run_scheduler())

if __name__ == "__main__":
    main()
    

