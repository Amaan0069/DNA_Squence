from fastapi import APIRouter, UploadFile, File, HTTPException
import csv
import io

# In-memory storage for uploaded data
data_store = {}

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    content = await file.read()
    decoded = content.decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(decoded))

    for row in csv_reader:
        try:
            sample_id = row["id"]
            data_store[sample_id] = {
                "region": row["region"],
                "age": row["age"],
                "seed": row["seed"]
            }
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing column in CSV: {e}")
    
    return {"message": "File uploaded and data parsed successfully.", "total_records": len(data_store)}
