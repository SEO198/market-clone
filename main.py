from fastapi import FastAPI,UploadFile,Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import os                      # 환경 변수 접근을 위한 모듈
from dotenv import load_dotenv
import sqlite3

load_dotenv()

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

# 배포할 때 다른 사람의 DB가 비어 있을 경우 자동으로 테이블을 생성하기 위해 IF NOT EXISTS를 사용
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)

app = FastAPI()

SECRET = os.environ.get("SECRET_KEY", "fallback_default_if_not_found")
manager = LoginManager(SECRET, '/login', use_cookie=True, cookie_name='access_token')

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENT = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENT = f'name="{data["name"]}"'
        
    # 컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENT}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str, Form()], 
           password:Annotated[str, Form()],
           # 쿠키 저장 로직 ------------------------------------------------------
           response: Response): # 👈 FastAPI Response 객체를 인수로 받습니다. 
            # ------------------------------------------------------------------=
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    # 액세스 토큰 발급 (생성)
    access_token = manager.create_access_token(data= {
        'sub': {
            'id':user['id'],
            'name':user['name'],
            'email':user['email']
        }
        
    })
    # 쿠키 저장 로직 ------------------------------------------------------
    # 2. HTTP 응답 헤더에 Set-Cookie 설정 (👈 추가된 로직)
    # httponly=True: JavaScript 접근 차단 (보안 강화)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600, # 쿠키 유효기간 (1시간)
        samesite="Lax" 
    )
    
    # 3. 토큰 대신 성공 메시지를 반환
    # 토큰은 이제 응답 본문이 아닌 HTTP 헤더(쿠키)로 전송됩니다.
    return {'message' : 'Login successful. Access token stored in cookie.'}
    # -----------------------------------------------------------------------
    # return {'access_token' : access_token} # json 토큰 저장방식일때 사용

    
    
    
@app.post('/signup')
def signup(id:Annotated[str, Form()], 
           password:Annotated[str, Form()],
           name:Annotated[str, Form()],
           email:Annotated[str, Form()]):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    return '200'


@app.post('/items')
async def create_item(image: UploadFile, 
                title: Annotated[str, Form()],
                price: Annotated[int, Form()],
                description: Annotated[str, Form()],
                place: Annotated[str, Form()],
                insertAt: Annotated[int, Form()],
                user=Depends(manager)):
    
    image_bytes = await image.read()    
    cur.execute(f"""
                INSERT INTO items(title, image, price, description, place, insertAt)
                VALUES ('{title}','{image_bytes.hex()}', {price},'{description}','{place}',{insertAt})
                """)
    con.commit()
    return '200'  

@app.get('/items')
async def get_items(user=Depends(manager)):
    # 컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                      SELECT * FROM items 
                      """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
    
    
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image FROM items WHERE id = {item_id}
                              """).fetchone()[0]    
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*')
    

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")