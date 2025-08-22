import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from fastapi import UploadFile
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("Cloudinary Cloud Name:", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("Cloudinary API Key:", os.getenv("CLOUDINARY_API_KEY"))
print("Cloudinary API Secret Present:", bool(os.getenv("CLOUDINARY_API_SECRET")))


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

async def upload_to_cloudinary(file: UploadFile):
    contents = await file.read()
    result = cloudinary.uploader.upload(contents, resource_type="auto")
    return result.get("secure_url")
