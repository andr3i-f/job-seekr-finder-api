import asyncio
from app.core.crons.scheduler import start_scheduler
import app.core.crons.crons

async def run_scheduler() -> None:
    start_scheduler()
    await asyncio.Event().wait()

def main():
    asyncio.run(run_scheduler())

if __name__ == "__main__":
    main()
    

