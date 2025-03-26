from fastapi import FastAPI, Depends, Form
from typing import Annotated
from fastapi.responses import JSONResponse, FileResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import csv
from dotenv import load_dotenv
import os
import json
from utils.dbSetup import initializeDB
from utils.auth import *

# JWT
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


load_dotenv()

app = FastAPI()

cur, conn = initializeDB(os.getenv("DB_USER"),  os.getenv("DB_HOST"), os.getenv("DB_NAME"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Internal API for Aspira"}

@app.post("/student/register")
async def register(data: dict):    
    regNo = data["no"]
    password = data["password"]
    sName = data["uname"]
    email = data["email"]
    phoneno = data["phoneno"]
    dob = data["dob"]
    cur.execute(f"SELECT regNo FROM Student WHERE regNo = \'{regNo}\'")
    if cur.rowcount > 0:
        return JSONResponse(status_code=400, content={"detail": "User already exists"})
    hashed_password = get_password_hash(password)
    print(hashed_password)
    cur.execute(f"INSERT INTO Student (regNo, sName, email, phoneno, dob) VALUES (\'{regNo}\', \'{sName}\', \'{email}\', \'{phoneno}\', \'{dob}\')")
    cur.execute(f"INSERT INTO Student_Pass (regNo, hashed_password) VALUES (\'{regNo}\', \'{hashed_password}\')")
    conn.commit()
    return JSONResponse(status_code=201, content={"detail": "User registered successfully"})

@app.post("/faculty/register")
async def register(data: dict):    
    fID = data["no"]
    password = data["password"]
    fName = data["uname"]
    email = data["email"]
    phoneno = data["phoneno"]
    dob = data["dob"]
    cur.execute(f"SELECT fID FROM Faculty WHERE fID = \'{fID}\'")
    if cur.rowcount > 0:
        return JSONResponse(status_code=400, content={"detail": "User already exists"})
    hashed_password = get_password_hash(password)
    print(hashed_password)
    cur.execute(f"INSERT INTO Faculty (fID, fName, email, phoneno, dob) VALUES (\'{fID}\', \'{fName}\', \'{email}\', \'{phoneno}\', \'{dob}\')")
    cur.execute(f"INSERT INTO Faculty_Pass (fID, hashed_password) VALUES (\'{fID}\', \'{hashed_password}\')")
    conn.commit()
    return JSONResponse(status_code=201, content={"detail": "User registered successfully"})

@app.post("/student/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    cur.execute(f"SELECT regNo, hashed_password FROM Student_Pass WHERE regNo = \'{data.username}\'")
    user = cur.fetchall()
    if cur.rowcount==0 or not verify_password(data.password, user[0][1]):
        return JSONResponse(status_code=401, content={"detail": "Incorrect username or password"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[0]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "category" : "student"}
    
@app.post("/faculty/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    cur.execute(f"SELECT fID, hashed_password FROM Faculty_Pass WHERE fID = \'{data.username}\'")
    user = cur.fetchall()
    if cur.rowcount==0 or not verify_password(data.password, user[0][1]):
        return JSONResponse(status_code=401, content={"detail": "Incorrect username or password"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[0]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "category" : "faculty"}

@app.post("/admin/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    cur.execute(f"SELECT aID, hashed_password FROM Admin_Pass WHERE aID = \'{data.username}\'")
    user = cur.fetchall()
    if cur.rowcount==0 or not verify_password(data.password, user[0][1]):
        return JSONResponse(status_code=401, content={"detail": "Incorrect username or password"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[0]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "category" : "admin"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = JSONResponse(
        status_code=401, content={"detail": "Could not validate credentials"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3123)
