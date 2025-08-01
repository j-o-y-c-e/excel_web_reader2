from fastapi import FastAPI,Form, UploadFile, File,Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
import io
# Initialize FastAPI application
app = FastAPI()

# Set up static files and templates 
app.mount("/static", StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Serve the main interface page
@app.get("/")
async def show_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_items/")
async def get_items(
    category: str = Form(...),
    file: UploadFile = File(...)
):
#process uploaded Excel file and return items from the first column
    try:
        # validate file extension
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code =400, detail="Just .xlsx files are accepted")
        # Construct file path
        file_path = os.path.join(DATA_DIR, f"{category}.xlsx")
        
        # Read Excel file using pandas
        df = pd.read_excel(io.BytesIO(await file.read()), engine = 'openpyxl')
        
        # Get items from the first column 
        items = df.iloc[:, 0].tolist()
        
        return JSONResponse({'success': True, 'items': items})
    
    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})
