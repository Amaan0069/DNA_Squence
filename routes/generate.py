# routes/generate.py

from fastapi import APIRouter, HTTPException
from utils.data_store import data_store
from func import generate_dna_sequence

router = APIRouter()

@router.get("/generate-sequence/{sample_id}")
async def generate_sequence(sample_id: str):
    if sample_id not in data_store:
        raise HTTPException(status_code=404, detail="Sample ID not found.")
    
    data = data_store[sample_id]
    sequence =  generate_dna_sequence(int(sample_id), data["region"], int(data["age"]), str(data["seed"]))
    
    return {"id": sample_id, "sequence": sequence}
