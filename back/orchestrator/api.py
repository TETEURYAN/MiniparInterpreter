from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from orchestrator.compiler import compile_code

router = APIRouter()

class CompileRequest(BaseModel):
    code: str
    export: bool = False

@router.post("/compile")
async def compile_endpoint(request: CompileRequest):
    try:
        result = compile_code(request.code, request.export)
        return {"status": "success", "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
