from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Define the response model
class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[dict]

# Function to return a JSON response
def json_response(status: str, message: str, data: Optional[dict] = None):
    response_model = ResponseModel(status=status, message=message, data=data)
    return JSONResponse(content=response_model.dict(), media_type="application/json")

# Function to return a successful response
def success_response(message: str, data: Optional[dict] = None):
    return json_response("success", message, data)

# Function to return an error response
def error_response(message: str, data: Optional[dict] = None):
    return json_response("error", message, data)

# Function to return a not found response
def not_found_response(message: str):
    return json_response("not found", message)

# Function to return a bad request response
def bad_request_response(message: str):
    return json_response("bad request", message)