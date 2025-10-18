from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
import secrets
import os
from datetime import datetime
from cryptography.fernet import Fernet
import db
import crud

router = APIRouter(prefix="/auth/canvas", tags=["canvas-auth"])

#Load env variables
CANVAS_CLIENT_ID = os.getenv("CANVAS_CLIENT_ID")
CANVAS_CLIENT_SECRET = os.getenv("CANVAS_CLIENT_SECRET");
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL");
CANVAS_REDIRECT_URI = os.getenv("CANVAS_REDIRECT_URI")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY");
FRONTEND_URL = os.getenv("FRONTEND_URL");

cipher = Fernet(ENCRYPTION_KEY)

oauth_states={}

def encrypt(text:str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrpyt(text:str) -> str:
    return cipher.decrypt(text.encode()).decode()

@router.get("/connect")

async def connect_canvas(user_id: int, database: Session = Depends(db.get_db)):


    user = crud.get_user(user_id); #Verify user exists

    if not user:
        raise HTTPException(status_code=404, detail="User not found");

    state = secrets.token_urlsafe(32);

    oauth_states[state]={
        "user_id": user_id,
        "created_at": datetime.now()
    }

    auth_url = (
        f"{CANVAS_BASE_URL}/login/oauth2/auth?"
        f"client_id={CANVAS_CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={CANVAS_REDIRECT_URI}&"
        f"state={state}"
        f"scope=url:GET|/api/v1/courses url:GET|/api/v1/assignments url:GET|/api/v1/users/self"

    )

    print(f"Redirecting user {user_id} to CanvasOauth)")
    return RedirectResponse(url = auth_url)


@router.get("/callback")

async def canvas_callback(code:str, state:str, database: Session = Depends(db.get_db)):

    print(f"Canvas Callback Successful");

    if state not in oauth_states:
        print("Invalid state")
        return RedirectResponse(f"{FRONTEND_URL}/settins?error=invalid_state")
    
    state_data = oauth_states.pop(state);
    user_id = state_data["user_id"]

    user = crud.get_user(database, user_id);
    if (not user):
        return RedirectResponse(f"{FRONTEND_URL}/settings?error=user_not_found")
    
    print(f"Getting access token");

    try:

        token_response = requests.post(
            f"{CANVAS_BASE_URL}/login/oauth2/token",
            data={
                "grant_type" : "authorization_code",
                "client_id": CANVAS_CLIENT_ID,
                "client_secret": CANVAS_CLIENT_SECRET,
                "redirect_uri": CANVAS_REDIRECT_URI,
                "code": code
                
            },
            timeout=10
        )

        if (token_response.status_code!=200):
            print(f"Token retrieval failed");
            return RedirectResponse(f"{FRONTEND_URL}/setttings?error=token_failed")
        
        token_data = token_response.json();
        access_token = token_response["access_token"]
        print("Token Retrieval Successful!!")
    except Exception as e:
        print(f"Exception during token retrieval: {e}");
        return RedirectResponse(f"{FRONTEND_URL}/setttings?error=token_failed")
    
    print("Verifying token");

    try:
        verify_response = requests.get("f{CANVAS_BASE_URL}/api/v1/users/self",
                                       headers={"Authorization": f"Bearer {access_token}",},
                                       timeout=10
        )
        if (verify_response.status_code!=200):
            print(f"Token verification failed");
            return RedirectResponse(f"{FRONTEND_URL}/settings?error=invalid_token")
        
        canvas_user = verify_response.json()
        print(f"Token verified for Canvas user: {canvas_user.get('name')}")
    except Exception as e:
        print(f"Token verificaiton failed: {e}")
        return RedirectResponse(f"{FRONTEND_URL}/settings?error=invalid_token")
    encrypt_token = encrypt(access_token)
    crud.update_canvas_token(db=database, user_id=user_id, canvas_token=access_token)

    print(f"Canvas connected successfully for user {user.name}")

    return RedirectResponse(f"{FRONTEND_URL}/dashboard")