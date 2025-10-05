from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
from app.core.openai_client import client, MODEL_NAME
from app.lib.util import extract_text_from_docx, extract_text_from_pdf
import os
import re

router = APIRouter()

system_prompt = """
    You are an HR and legal expert helping a fresher review a company's offer letter.
    Analyze the document and return your findings **strictly in JSON format** with the following structure:

    {
      "good_policies": [ ... ],
      "policies_to_negotiate": [ ... ],
      "red_flags": [ ... ],
      "missing_benefits_or_points_of_concern": [ ... ],
      "career_growth_opportunities": [ ... ],
      "work_life_balance_insights": [ ... ],
      "final_conclusion": "..."
    }

    Notes:
    - Be objective, concise, and clear.
    - If a section is missing, return an empty array for that field.
    - Mention specific clauses or policy names when possible.
"""

# TODO: read doc in chunks for large documents.
# TODO: add database logging
@router.post("/review-offer-letter/")
async def review_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = ""

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif file.filename.endswith(".docx"):
        with open("temp.docx", "wb") as f:
            f.write(file_bytes)
        text = extract_text_from_docx("temp.docx")
        os.remove("temp.docx")
    else:  # treat as plain text
        text = file_bytes.decode("utf-8")

    if not text.strip():
        return JSONResponse({"error": "Could not extract text from document"}, status_code=400)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze the following job policy document:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=1000
    )

    raw_output = response.choices[0].message.content
    sanitized_output = re.sub(r"^```(json)?|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

    try:
        import json
        parsed = json.loads(sanitized_output)
        return parsed
    except:
        # Return raw text if not valid JSON
        return {"raw_output": raw_output, "warning": "Could not parse perfect JSON"}