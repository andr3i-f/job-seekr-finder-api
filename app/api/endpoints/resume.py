from fastapi import APIRouter, Depends, UploadFile, File
from groq import AsyncGroq
import pdfplumber
import io

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.consts import GROQ_PARSE_TEXT_PROMPT

router = APIRouter()

client = AsyncGroq(
    api_key=get_settings().general.groq_api_key.get_secret_value()
)

def extract_text(file_bytes: bytes) -> str:
    text = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as f:
        for page in f.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text) 

    return "\n".join(text)

async def parse_with_llm(text) -> str:
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": GROQ_PARSE_TEXT_PROMPT.format(text)}],
        model="llama-3.1-8b-instant",
        temperature=0
    )
        
    return response

@router.post("/parse-resume")
async def parse_resume(
    resume: UploadFile = File(...)
):
    print(resume)
    # parse into a variable called text
    # text = extract_text(resume)
    # parsed_text = parse_with_llm(text)

    return { "parsed": "200" }


