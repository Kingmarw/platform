from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from pywebio.input import file_upload
from pywebio.output import put_text
from pywebio.platform.fastapi import asgi_app
from fastapi.staticfiles import StaticFiles
import os, json

# فولدر التخزين
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ملف JSON لحفظ الفيديوهات
DATA_FILE = "videos.json"

# لو الملف مش موجود نعمله فاضي
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


# دالة للقراءة من JSON
def load_videos():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# دالة للكتابة في JSON
def save_videos(videos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)


# صفحة الرفع بالـ PyWebIO
def upload_page():
    file = file_upload("ارفع فيديو", accept="video/*")
    file_path = os.path.join(UPLOAD_DIR, file['filename']) # type: ignore
    with open(file_path, "wb") as f:
        f.write(file['content']) # type: ignore
    inp = input("اسم الفيديو")
    videos = load_videos()
    videos.append({
        "title": inp, # type: ignore
        "url": f"/uploads/{file['filename']}" # type: ignore
    })
    save_videos(videos)

    put_text("تم رفع الفيديو وحفظه بنجاح ✅")


# FastAPI app
app = FastAPI()

# ربط PyWebIO كـ app داخل FastAPI
app.mount("/admin", asgi_app(upload_page))

# API ترجع الفيديوهات
@app.get("/api/videos")
def get_videos():
    return JSONResponse(load_videos())


@app.get("/", response_class=HTMLResponse)
def home():
    file_path = os.path.join("web", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# تقديم الملفات المرفوعة (static)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")



