# [jobseekr.dev](https://jobseekr.dev/) backend (Senior Project)

## Application Outline ( to potentially be revised )

This is the backend service that is responsible for scraping, storing and sending job information, and resume parsing.

This service utilizes FastAPI, dev/testing PostgreSQL database (to mimick the production database hosted on heroku), crons for the scrapers, and authenticates JWTs from the frontend.

This repository is templated from: https://github.com/rafsaf/minimal-fastapi-postgres-template

## Local Development 

1. Clone the repository
2. Copy .env.example to .env
3. Run:

```bash
~/dev/sp/job-seekr-finder-api main ❯ docker compose up -d --build                                                                                   08:55:32 PM
Compose now can delegate build to bake for better performances
Just set COMPOSE_BAKE=true
[+] Building 1.0s (23/23) FINISHED
...
```

4. To enter the backend container, run:

```bash
~/dev/sp/job-seekr-finder-api main ❯ docker compose exec backend bash                                                                               08:55:36 PM

root@19ef24410c42:/build#
```

and run supervisord to start the service:

```bash
root@19ef24410c42:/build# supervisord -n
```

### Formatting

In the backend container, run:

```bash
root@19ef24410c42:/build# ruff format
```