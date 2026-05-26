from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Pydantic 모델
class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def read_data():
    if not os.path.exists("courses.json"):
        return []
    try:
        with open("courses.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def write_data(data):
    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# GET 데이터 반환해주기
@app.get("/courses")
async def get_courses():
    return read_data()

# POST 수강 기록 추가
@app.post("/courses")
async def add_course(course: Course):
    try:
        data = read_data() # 데이터 읽고
        
        new_course = course.model_dump()
        data.append(new_course)
        write_data(data) # new_course 끼운걸로 다시 적기.
        
        return {
            "msg": "course added successfully",
            "data": new_course
        }
    except Exception as e:
        raise HTTPException(status_code=500) # FastAPI에서 raise는 서버를 중지하지 않고
                                            # 로직을 중단하고 클라이언트에게 에러 응답을 보내는 도구임.
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)