import asyncio
from datetime import UTC, datetime, timedelta

import resend
from sqlalchemy import desc, or_, select

from app.core.config import get_settings, logger
from app.core.consts import (
    JOB_SEEKR_DASHBOARD,
    RESEND_JOB_TEMPLATE_HTML,
    JobExperienceToResendSegmentID,
    JobExperienceTypes,
)
from app.core.database_session import get_async_session
from app.models import Job


def _initialize_resend_api_key() -> None:
    resend.api_key = get_settings().general.resend_key.get_secret_value()


class Email:
    def __init__(self):
        self.JOBS_IN_EMAIL_LIMIT = 5
        _initialize_resend_api_key()

    async def send_emails(self):
        for experience_type in JobExperienceTypes:
            if experience_type == JobExperienceTypes.SENIOR:
                # Skip because senior and mid-level are concatenated when sending emails
                continue

            await self.send_email(experience_type)
            await asyncio.sleep(5)

    async def send_email(self, experience_level: JobExperienceTypes):
        variables = await self.get_email_variables(experience_level)

        if "NUM_OF_JOBS" not in variables or variables["NUM_OF_JOBS"] == 0:
            return

        html_content = RESEND_JOB_TEMPLATE_HTML
        for key, value in variables.items():
            placeholder = f"{{{{{{{key}}}}}}}"
            html_content = html_content.replace(placeholder, str(value))

        params: resend.Broadcasts.CreateParams = {
            "segment_id": JobExperienceToResendSegmentID[experience_level.name].value,
            "from": "Jobs <jobs@jobseekr.dev>",
            "subject": "jobseekr - Daily Jobs Reporting",
            "html": html_content,
            "send": True,
        }

        try:
            await asyncio.to_thread(resend.Broadcasts.create, params)
        except resend.exceptions.ValidationError as e:
            if "audience you are sending has no contacts" in str(e):
                return
            logger.error(f"Error creating broadcast: {e}")
            return

        logger.info(
            f"EMAIL SERVICE: Sent emails using Resend for experience level: {'Mid-Level/Senior' if experience_level.value == 'Mid-Level' else experience_level.value}"
        )

    async def get_email_variables(self, experience_level: JobExperienceTypes):
        return {
            "DASHBOARD": JOB_SEEKR_DASHBOARD,
            **(await self.get_recent_jobs(experience_level)),
        }

    async def get_recent_jobs(self, experience_level: JobExperienceTypes):
        query = self.get_job_query(experience_level)

        async with get_async_session() as session:
            result = await session.execute(query)
            jobs = result.scalars().all()

        return {"NUM_OF_JOBS": len(jobs), **(self.get_email_jobs(jobs))}

    def get_job_query(self, experience_level: JobExperienceTypes):
        one_day = datetime.now(UTC) - timedelta(days=1)

        query = (
            select(Job)
            .order_by(desc(Job.create_time))
            .where(Job.create_time >= one_day)
        )

        if experience_level == JobExperienceTypes.MID_LEVEL:
            # Query for mid-level OR senior for email notifs due to Resend free tier 3 segment limitation
            return query.where(
                or_(
                    Job.experience_level == JobExperienceTypes.MID_LEVEL.value,
                    Job.experience_level == JobExperienceTypes.SENIOR.value,
                )
            )

        return query.where(Job.experience_level == experience_level.value)

    def get_email_jobs(self, jobs: list[Job]):
        email_jobs = {}

        jobs_to_include = jobs[: self.JOBS_IN_EMAIL_LIMIT]
        for index, job in enumerate(jobs_to_include):
            email_jobs[f"JOB_{index + 1}"] = (
                f"<a href='{job.url}'>{job.company_name} - {job.title} - {job.location}</a>"
            )

        email_jobs["NUM_OF_JOBS_IN_EMAIL"] = len(jobs_to_include)

        return email_jobs
