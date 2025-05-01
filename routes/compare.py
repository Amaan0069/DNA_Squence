from fastapi import APIRouter, HTTPException
from models import CompareRequest
from utils.data_store import data_store
from func import generate_dna_sequence
from utils.compare_logic import compare_sequences

router = APIRouter()

@router.post("/compare-sequences/")
async def compare_sequences_api(req: CompareRequest):
    id1, id2 = req.id1, req.id2
    
    if id1 not in data_store or id2 not in data_store:
        raise HTTPException(status_code=404, detail="One or both sample IDs not found.")
    
    data1, data2 = data_store[id1], data_store[id2]
    
    seq1 = generate_dna_sequence(id1, data1["region"], data1["age"], data1["seed"])
    seq2 = generate_dna_sequence(id2, data2["region"], data2["age"], data2["seed"])
    
    score = compare_sequences(seq1, seq2)
    
    return {
        "sample1": id1,
        "sample2": id2,
        "similarity_score": f"{score} %"
    }
