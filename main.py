from fastapi import UploadFile, FastAPI,HTTPException, Request,Form
from fastapi.responses import JSONResponse, HTMLResponse,RedirectResponse, FileResponse
from pywebio.input import file_upload, input
from pywebio.output import put_text,put_html,put_info
from pywebio.platform.fastapi import asgi_app
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os, json, cloudinary, cloudinary.uploader
import tempfile
import random
import os, json, shutil, cloudinary, cloudinary.uploader
from urllib.parse import quote, unquote
cloudinary.config( 
  cloud_name = "ddzvcwo9v", 
  api_key = "274515435158953", 
  api_secret = "4M5xR5S9OL5E8dpjlLUlFn_BY_I" 
)

app = FastAPI()
app.mount("/web", StaticFiles(directory="web"), name="web")

# ملفات JSON لكل صف
DATA_FILES = {
    "p1": "p1.json",
    "p2": "p2.json",
    "p3": "p3.json"
}

# لو الملفات مش موجودة نعملها
for f in DATA_FILES.values():
    if not os.path.exists(f):
        with open(f, "w", encoding="utf-8") as file:
            json.dump([], file)

# دوال مساعدة
def load_videos(grade):
    with open(DATA_FILES[grade], "r", encoding="utf-8") as f:
        return json.load(f)

def save_videos(grade, videos):
    with open(DATA_FILES[grade], "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

# ---------------------- API رفع الفيديو ----------------------
@app.post("/api/upload/{grade}")
async def upload_video(
    grade: str,
    title: str = Form(...),
    video: UploadFile = Form(...),
    thumb: UploadFile = Form(...)
):
    if grade not in DATA_FILES:
        return JSONResponse({"error": "الصف غير موجود"}, status_code=400)

    # حفظ الملفات مؤقتًا
    video_path = f"temp_{video.filename}"
    thumb_path = f"temp_{thumb.filename}"

    with open(video_path, "wb") as f:
        shutil.copyfileobj(video.file, f)
    with open(thumb_path, "wb") as f:
        shutil.copyfileobj(thumb.file, f)

    # رفع الفيديو
    upload_video_res = cloudinary.uploader.upload_large(video_path, resource_type="video")
    video_url = upload_video_res.get("secure_url")

    # رفع الصورة
    upload_thumb_res = cloudinary.uploader.upload(thumb_path, resource_type="image")
    thumb_url = upload_thumb_res.get("secure_url")

    # مسح الملفات المؤقتة
    os.remove(video_path)
    os.remove(thumb_path)

    # حفظ في JSON
    videos = load_videos(grade)
    videos.append({
        "title": title,
        "url": video_url,
        "thumbnail": thumb_url
    })
    save_videos(grade, videos)

    return {
        "message": "✅ تم رفع الفيديو بنجاح",
        "title": title,
        "video_url": video_url,
        "thumb_url": thumb_url
    }

# ---------------------- API عرض الفيديوهات ----------------------
@app.get("/api/videos/{grade}")
def get_videos(grade: str):
    if grade not in DATA_FILES:
        return JSONResponse({"error": "الصف غير موجود"}, status_code=400)
    return JSONResponse(load_videos(grade))

@app.get("/grade/1",response_class=HTMLResponse)
def grade1():
    return FileResponse("web/p1.html")
@app.get("/grade/2",response_class=HTMLResponse)
def grade2():
    return FileResponse("web/p2.html")
@app.get("/grade/3",response_class=HTMLResponse)
def grade3():
    return FileResponse("web/p3.html")
@app.get("/upload/1",response_class=HTMLResponse)
def upload1():
    return FileResponse("web/upload.html")
@app.get("/upload/2",response_class=HTMLResponse)
def upload2():
    return FileResponse("web/upload2.html")
@app.get("/upload/3",response_class=HTMLResponse)
def upload3():
    return FileResponse("web/upload3.html")




DB_FILE = "data.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if request.cookies.get("session") == "logged":
        file_path = os.path.join("web", "index.html")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        username = request.cookies.get("username", "")
        username = unquote(username)

        content = content.replace("{{username}}", username)

        return HTMLResponse(content)

    return FileResponse("web/index.html")


@app.get("/lo", response_class=HTMLResponse)
def login_page(request: Request):
    if request.cookies.get("session") == "logged":
        return RedirectResponse(url="/")
    return FileResponse("web/login.html")

@app.get("/si", response_class=HTMLResponse)
def sign_page(request: Request):
    if request.cookies.get("session") == "logged":
        return RedirectResponse(url="/lo")
    return FileResponse("web/signup.html")



@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    for user in users:
        if user["username"] == username and user["password"] == password:
            response = RedirectResponse(url="/", status_code=302)
            response.set_cookie(key="session", value="logged", httponly=False)
            response.set_cookie(key="username", value=quote(username), httponly=False)
            return response

    return RedirectResponse(url="/lo?error=1", status_code=302)

@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    with open(DB_FILE,"r",encoding="utf-8") as f:
        users = json.load(f)
    if any(user['username'] == username for user in users):
        return {"error":"username already exisits"}
    
    users.append({"username":username,"password":password})
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(users,f,ensure_ascii=False,indent=2)
    return RedirectResponse(url="/lo", status_code=302)
    
@app.exception_handler(404)
async def not_found(request: Request,exc):
    with open('web/404.html',"r",encoding="utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content,status_code=404)



@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/lo")
    response.delete_cookie("session")
    response.delete_cookie("username")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
