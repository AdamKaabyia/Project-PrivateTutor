from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Constants for Google OAuth2
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback/google"
SCOPES = "https://www.googleapis.com/auth/calendar.readonly"
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# OAuth2 scheme for FastAPI
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}",
    tokenUrl=TOKEN_URL,
    refreshUrl=TOKEN_URL,
    scheme_name="Google"
)

@app.get("/auth/login/google")
def login():
    return RedirectResponse(url=f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}")

@app.get("/auth/callback/google")
async def callback(code: str = Depends(oauth2_scheme)):
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=payload)
        response.raise_for_status()
        tokens = response.json()
    return tokens

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
