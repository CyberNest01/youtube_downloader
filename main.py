import uvicorn
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
import aiofiles

from controller import youtube_downloader

import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="template")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def iterfile(file_path: str):
    async with aiofiles.open(file_path, 'rb') as file:
        while chunk := await file.read(1024 * 1024):
            yield chunk


@app.post("/submit-form")
async def submit_form(
    url: str = Form(...),
    url_type: int = Form(...),
    resolution: str = Form(...)
):
    path_list = await youtube_downloader(url, url_type, resolution)
    if path_list and os.path.exists(path_list):
        # headers = {
        #     'Content-Disposition': f'attachment; filename="{os.path.basename(path_list)}"',
        #     'Content-Type': 'application/octet-stream'
        # }
        # return StreamingResponse(iterfile(path_list), headers=headers)
        return FileResponse(path_list)
    raise HTTPException(status_code=400, detail="Not found !!!")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=4, http='h11', loop="uvloop")
