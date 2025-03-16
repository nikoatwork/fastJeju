# FastJeju

A FastAPI project with Pydantic and Pandas integration.

## What this repo contains

- Python environment setup with virtualenv
- FastAPI with example endpoints
- Pydantic for data validation
- Pandas for data manipulation

## Setup

### 1. Install Python and virtualenv

#### For Mac:
```bash
# Install Python if not already installed
brew install python

# Install virtualenv
pip install virtualenv
```

#### For Windows:
```bash
# Install Python from https://www.python.org/downloads/
# Then install virtualenv
pip install virtualenv
```

### 2. Create a virtual environment

```bash
virtualenv venv
```

### 3. Activate the environment

#### For Mac/Linux:
```bash
source venv/bin/activate
```

#### For Windows:
```bash
# In Command Prompt:
venv\Scripts\activate.bat

# In PowerShell:
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify installation
```bash
python -c "import fastapi, pydantic, pandas; print('Installation successful!')"
```

## Running the application

Start the FastAPI server:

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Running tests

(currently no tests written)

```bash
pytest
```

## API Endpoints

- `GET /`: Root endpoint
- `GET /api/items`: Get all items
- `GET /api/items/{item_id}`: Get a specific item
- `POST /api/items`: Create a new item
- `GET /api/pandas/info`: Get information about the pandas DataFrame

# How you can make this repo useful for you

## Getting started with this template

1. **Copy the repository**
   ```bash
   git clone https://github.com/username/fastJeju.git my-project
   cd my-project
   git remote remove origin
   git remote add origin YOUR_NEW_REPO_URL
   git push -u origin main
   ```

2. **Study the example endpoints**
   - Examine the structure in `app/routers/`
   - See how validation works with Pydantic models in `app/models/`
   - Understand the data flow from request to response

3. **Create your own endpoint**
   - Copy an existing endpoint as a starting point
   - Modify the route, request/response models, and logic
   - Example:
     ```python
     @router.post("/api/custom", response_model=models.CustomResponse)
     def create_custom_data(data: models.CustomRequest):
         result = process_data(data)
         return models.CustomResponse(id=uuid4(), result=result)
     ```

4. **Implement data processing with Pandas**
   - Create a new service in `app/services/`
   - Use Pandas for data manipulation, analysis, or visualization
   - Example service:
     ```python
     # app/services/analysis_service.py
     import pandas as pd

     def analyze_data(dataset: pd.DataFrame):
         # Perform calculations, transformations, aggregations
         summary = dataset.describe()
         trends = dataset.groupby('category').mean()
         return {
             "summary": summary.to_dict(),
             "trends": trends.to_dict()
         }
     ```

5. **Expose your data service via API**
   - Connect your service to an endpoint
   - Format the results for API consumption
   - Add proper error handling
   - Example:
     ```python
     @router.post("/api/analyze")
     def analyze_dataset(file: UploadFile):
         try:
             content = await file.read()
             df = pd.read_csv(io.StringIO(content.decode('utf-8')))
             result = analysis_service.analyze_data(df)
             return result
         except Exception as e:
             raise HTTPException(status_code=400, detail=str(e))
     ```

6. **Deploy your application**
  - (working on this)
