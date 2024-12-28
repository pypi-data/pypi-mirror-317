from urllib.parse import urlencode
from typing import Dict, Any
import json
from pydantic import BaseModel

def dictToQueryParams(params: Dict[str, any]) -> str:
    formattedParams = {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in params.items() if v is not None}
    return urlencode(formattedParams)

def jsonToQueryParams(params: str) -> str:
    try:
        dictParams = json.loads(params)
        return dictToQueryParams(dictParams)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input for query parameters")
    
def parseToQueryParams(params: any) -> str:
    if isinstance(params, BaseModel):
        params = params.model_dump()
        return dictToQueryParams(params)
    if isinstance(params, dict):
        return dictToQueryParams(params)
    elif isinstance(params, str):
        return jsonToQueryParams(params)
    else:
        raise ValueError("Unsupported input type for query parameters")