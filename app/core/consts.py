from enum import Enum


class JobExperienceTypes(str, Enum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    MID_LEVEL = "Mid-Level"
    SENIOR = "Senior"


STATUS_CODE_200 = 200

GROQ_PARSE_TEXT_PROMPT = """
Extract structured tech resume data as JSON with:
- skills (list)
- experience level (string and it can only be: 'Intern', 'Junior', 'Mid-Level', or 'Senior'. This is based off of information from the resume, such as if they graduated or YOE working in the tech industry)


Return ONLY valid JSON in this exact format:

{
  "skills": [string],
  "experience_level" string
}

Resume:
{}
"""