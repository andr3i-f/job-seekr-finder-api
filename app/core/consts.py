from enum import Enum


class JobExperienceTypes(str, Enum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    MID_LEVEL = "Mid-Level"
    SENIOR = "Senior"


STATUS_CODE_200 = 200

GROQ_PARSE_TEXT_PROMPT = f"""
Extract structured resume data as JSON with:
- name
- email
- phone
- skills (list)
- education (list)
- experience (list of jobs)


Return ONLY valid JSON in this exact format:

{
  "name": string,
  "email": string,
  "phone": string,
  "skills": [string],
  "education": [string],
  "experience": [
    {
      "title": string,
      "company": string,
      "years": string
    }
  ]
}

Resume:
{text}
"""