import io
import json
import re

import pdfplumber
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from groq import AsyncGroq
from groq.types.chat import ChatCompletion

from app.api.deps import get_current_user
from app.core.config import get_settings, logger
from app.core.consts import GROQ_PARSE_TEXT_PROMPT, GROQ_SYSTEM_PROMPT

router = APIRouter()

client = AsyncGroq(api_key=get_settings().general.groq_api_key.get_secret_value())


def extract_text(file_bytes: bytes) -> str:
    text = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as f:
        for page in f.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return "\n".join(text)


async def parse_with_llm(text) -> ChatCompletion:
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": GROQ_SYSTEM_PROMPT},
            {"role": "user", "content": GROQ_PARSE_TEXT_PROMPT.format(text)},
        ],
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    return response


@router.post("/parse-resume")
async def parse_resume(resume: UploadFile = File(...), _=Depends(get_current_user)):
    file_bytes = await resume.read()
    text = extract_text(file_bytes)
    parsed_text = await parse_with_llm(text)

    raw_content = parsed_text.choices[0].message.content

    try:
        cleaned_content = re.search(r"\{.*\}", raw_content, re.DOTALL)
        if cleaned_content:
            cleaned_content = cleaned_content.group(0)
            parsed_data = json.loads(cleaned_content)

            return {"parsed": parsed_data}

    except (json.JSONDecodeError, ValueError) as e:
        logger.exception(f"Error occurred trying to parse resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse output",
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error parsing resume...",
    )
