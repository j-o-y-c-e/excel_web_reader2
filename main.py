from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

# Create the main application
app = FastAPI()

# Setup for website files (CSS, JS) and HTML templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Directory where Excel files are stored
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Show the main webpage
@app.get("/")
async def show_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/get_categories')
async def get_categories():
    """Returns list of available categories (Excel/CSV files without extensions)"""
    try:
        # List all Excel/CSV files in the data directory
        files = []
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.xlsx') or filename.endswith('.csv'):
                name_only = os.path.splitext(filename)[0]  # Remove extension
                files.append(name_only)
        return JSONResponse({'success': True, 'categories': files})
    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})

@app.post('/get_columns')
async def get_column_name(request: Request):
    """Returns column names for a specific category/file"""
    try:
        # Get category from request form data
        form_data = await request.form()
        category = form_data.get('category')
        
        if not category:
            return JSONResponse({'success': False, 'error': 'No category provided'})
        
        # Search for file with supported extensions
        for ext in ['.xlsx', '.csv']:
            file_path = os.path.join(DATA_DIR, f"{category}{ext}")
            if os.path.exists(file_path):
                # Read file based on extension type
                if ext == '.xlsx':
                    df = pd.read_excel(file_path, engine='openpyxl')
                else:
                    df = pd.read_csv(file_path)
                return JSONResponse({'success': True, 'columns': list(df.columns)})
        
        return JSONResponse({'success': False, 'error': 'File not found'})
        
    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})

@app.post('/get_items')
async def get_items(request: Request):
    """Returns items from a specific column in a file"""
    try:
        # Get parameters from request form data
        form_data = await request.form()
        category = form_data.get('category')
        column_name = form_data.get('column_name')
        
        if not category or not column_name:
            return JSONResponse({'success': False, 'error': 'Missing category or column parameter'})
        
        # Find file with correct extension
        file_path = None
        for ext in ['.xlsx', '.csv']:
            temp_path = os.path.join(DATA_DIR, f"{category}{ext}")
            if os.path.exists(temp_path):
                file_path = temp_path
                break
        
        if not file_path:
            return JSONResponse({'success': False, 'error': 'File not found'})
        
        # Read file based on extension type
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl', header=0)
        else:
            df = pd.read_csv(file_path, header=0)
        
        # Verify requested column exists
        if column_name not in df.columns:
            return JSONResponse({
                'success': False,
                'error': f"Column '{column_name}' not found",
                'available_columns': list(df.columns)
            })
        
        # Get all non-null values from the specified column
        items = df[column_name].dropna().tolist()
        
        return JSONResponse({
            'success': True,
            'items': items,
            'columns': list(df.columns)
        })
    
    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})
