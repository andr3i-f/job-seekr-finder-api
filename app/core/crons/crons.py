from .scheduler import scheduler

from app.core.scrapers.adzuna import Adzuna

adzuna = Adzuna()

async def adzuna_scraper_cron():
    await adzuna.call()

scheduler.add_job(
    adzuna_scraper_cron,
    trigger="cron",
    minute="*",
    id="adzuna_scraper_cron",
    misfire_grace_time=3600,
    replace_existing=True 
)