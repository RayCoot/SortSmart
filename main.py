import os
import subprocess
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import RedirectResponse, FileResponse
from starlette.staticfiles import StaticFiles

from AppConfig import APP_API_PORT
from LoggingUtil import get_logger
from scanner import query_recycle_method_from_image

load_dotenv()
logger = get_logger("main")

UPLOAD_DIR = Path("/work/temp-data")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()

# Optional: Handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
async def read_index():
    file_path = "static/index.html"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="HTML file not found")
    return FileResponse(path=file_path,media_type="text/html")


# Define the JSON payload structure
class ImageMetadata(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None


# Route to upload image + JSON metadata
@app.post("/api/upload-image")
async def upload_image(
        image: UploadFile = File(...),
        metadata: str = Form(...)
):
    # Parse JSON metadata
    import json
    metadata_dict = json.loads(metadata)
    logger.info(f"upload-image received json: {metadata_dict}")
    # Read image content
    image_content = await image.read()
    logger.info(f"upload-image received image filename: {image.filename}")
    if len(image_content) > 80000:
        raise HTTPException(status_code=400, detail="image too large, image size must smaller than 80,000 bytes")

    logger.debug(f"Received image: {image.filename}, size: {len(image_content)} bytes, Metadata: {metadata_dict}")
    if "city" not in metadata_dict.keys() and "region" not in metadata_dict.keys():
        logger.info(f"both city and region empty or none")
        raise HTTPException(status_code=400, detail="both city and region empty or none, must provide either one")

    city = metadata_dict.get("city","")
    region = metadata_dict.get("region","")
    ret = query_recycle_method_from_image(image_content, city, region)
    logger.info(f"query_dispose_instruction: {ret}")
    return {
        "filename": image.filename,
        "content_type": image.content_type,
        "metadata": metadata_dict,
        "response": ret
    }


if __name__ == "__main__":
    subprocess.run(["uvicorn", "main:app",
                    "--host", "0.0.0.0", "--port", f"{APP_API_PORT}", "--reload"])
    # Start the Uvicorn server from code

# To run the FastAPI app:
# uvicorn filename:app --reload
