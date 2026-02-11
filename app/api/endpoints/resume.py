from fastapi import APIRouter, Depends
from groq import AsyncGroq

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.consts import GROQ_PARSE_TEXT_PROMPT

router = APIRouter()

client = AsyncGroq(
    api_key=get_settings().general.groq_api_key.render_as_string(hide_password=False)
)

def extract_text(file) -> str:
    return ""

async def parse_with_llm(text) -> str:

    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": GROQ_PARSE_TEXT_PROMPT.format(text)}],
        model="llama-3.1-8b-instant",
        temperature=0
    )
        
    return ""

@router.get("/parse-resume")
async def parse_resume(
    resume,
    _=Depends(get_current_user)
):
    # parse into a variable called text
    text = extract_text(resume)
    parsed_text = parse_with_llm(text)

    return { "parsed": parsed_text }


