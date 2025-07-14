from fastapi import FastAPI,Form, UploadFile, File,Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
import io

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
@app.get("/")
async def show_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_items/")
async def get_items(
    category: str = Form(...),
    file: UploadFile = File(...)
):
    
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code =400, detail="Just .xlsx files are accepted")
        # Construct file path
        file_path = os.path.join(DATA_DIR, f"{category}.xlsx")
        
        # Read Excel file
        df = pd.read_excel(io.BytesIO(await file.read()), engine = 'openpyxl')
        
        # Get the first column (assuming single column files)
        items = df.iloc[:, 0].tolist()
        
        return JSONResponse({'success': True, 'items': items})
    
    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})


