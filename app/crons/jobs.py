import requests
from .scheduler import scheduler
from app.core.config import get_settings

def call_adzuna_api():
    print(f"adzuna application id - {get_settings().adzuna.application_id}")
    print(f"adzuna application key - {get_settings().adzuna.application_key}")

    payload = {
        'app_id': get_settings().adzuna.application_id,
        'app_key': get_settings().adzuna.application_key,
        'results_per_page': 100,
        'what': 'Software Developer',
        'location': 'Oregon'
    }
    page = 1
    country = 'us'
    
    # Call the adzuna api
    res = requests.get(f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}", params=payload)

    # Collect information
    if 'results' in res:
        for x in res['results']:
            print(x['title'])
            print(x['location'])
            print(x['company']['display_name'])
            print(f"{x['salary_min']} - {x['salary_max']}")
            print("      ")
    # Create jobs

    # store them into database

scheduler.add_job(
    call_adzuna_api,
    trigger="cron",
    minute="*",
    id="call_adzuna_api",
    misfire_grace_time=3600,
    replace_existing=True 
)
