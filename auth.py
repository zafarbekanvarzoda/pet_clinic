from fastapi import Header, HTTPException

CREATE_KEY = "create-2026"
READ_KEY = "read-2026"
UPDATE_KEY = "update-2026"
DELETE_KEY = "delete-2026"

def verify_create_api_key(x_api_key: str = Header()):
    if x_api_key != CREATE_KEY:
        raise HTTPException(status_code = 403, detail="Invalid API Key")

def verify_read_api_key(x_api_key: str = Header()):
    if x_api_key != READ_KEY:
        raise HTTPException(status_code = 403, detail="Invalid API Key")

def verify_update_api_key(x_api_key: str = Header()):
    if x_api_key != UPDATE_KEY:
        raise HTTPException(status_code = 403, detail="Invalid API Key")

def verify_delete_api_key(x_api_key: str = Header()):
    if x_api_key != DELETE_KEY:
        raise HTTPException(status_code = 403, detail="Invalid API Key")


