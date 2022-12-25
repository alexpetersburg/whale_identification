import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from tools import IdentificationBytes

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.post("/upload_files")
async def upload(files: List[UploadFile] = File(...)):
    for img_remove in [i for i in os.listdir("temp") if i.endswith(".jpg")]:
        os.remove("temp/" + img_remove)
    for file in files:
        contents = await file.read()
        img = IdentificationBytes()
        img.cos(contents)


@app.get("/get_mask")
def get_img():
    PATH = Path("temp")
    PATH_OUT = [x for x in PATH.glob("**/*.jpg")][-1]
    return FileResponse(PATH_OUT)
