# --------------------------------------------
# 파일명: task.py
# 위치: api/routers/task.py
# 이 파일은 "할 일(ToDo)" 기능을 처리하는 API를 정의한한 곳이다.
# - /tasks로 시작하는 주소들을 FastAPI의 APIRouter로 관리하다.
# - 주요 기능: 할 일 목록 조회, 할 일 추가, 수정 삭제제
# --------------------------------------------

# * FastAPI에서 여러 개의 URL 경로를 그룹으로 묶어 관리할 수 있게 해주는 도구
from fastapi import APIRouter, Depends, HTTPException
# - APURouter: 기능별로 URL을 나눠 관리할 수 있게 해줌 (예: /tasks, /users 등)
# - Depends: 다른 함수(예: DB 연결)를 자동으로 실행하고 주입해주는 도구

#   * SQLAlecmy dml 비동기 세션을 사용하기 위한 도구
from sqlalchemy.ext.asyncio import AsyncSession
# - AsybcSession: await를 사용하는 비동기 DB 작업에 사용됨

# * 우리가 만든 CRUD 함수들을 불러온다 (파일 위치: api/cruds/task.py)
# - FastAPI에서 Depends로 연결할 수 있게 준비해둔 함수
# - 비동기 세션(AsyncSession)을 변환함
import api.cruds.task as task_crud

# * 우리가 정의한 데이터 구조를 불러온다 (파일 위치: api/db.py)
# - FastAPI에서 Depends로 연결할 수 있게 준비해둔 함수
# - 비동기 세션(AsyncSession)을 변환함
from api.db import get_db

# * 우리가 정의한 데이터 구조를 불러온다 (파일 위치: api/scema/task.py)
# - Task : 전체 할 일 데이터를 표현
# - TaskCreate: 사용자가 보낼 입력 데이터 구조
# - TaskCreateResponse: 응답할 때 사용할 데이터 구조 (id 포험)
import api.schemas.task as task_schema

# * router 객체를 만든다
# - task 목록과 관련된 여러 기능을 이 객체에 모두 담아서
#   나중에 main.py에서 FaskAPI 앱에 등록하게 된다.
router=APIRouter()

# -----------------------------
# [1] 할 일 목록 조회 (GET 요청청)
# - 클라이언트가 /tasks 주소로 요청하면 전체 할 일 목록을 변환한다.
# - 아직 DB는 연결하지 않았기 때문에 임시 데이터만 보여준다.
# -----------------------------
@router.get("/tasks",response_model=list[task_schema.Task])
# - response_model: 응답의 데이터 형태를 지정함
# - 여기서는 Task 모델을 여러 개 답은 리스트르 변환한다고 지정함
async def list_tasks():
    return[
        task_schema.Task(id=1,title="첫 번째 ToDo 작업",done=False)
    ]
    # * Task 모델 형식에 맞는 임시 데이터를 리스트 형태로 만들어 변환함
    # * 실제 DB 연동 시에는 DB에서 데이터를 꺼내서 여기에 넣을 예정

# ------------------------------
# [2] 할 일 추가 기능 (POST 요청)
# - 클라이언트가 JSON 형식으로 보낸 데이터(title)를 받아
#   새로운 할 일을 생성하는 기능 (예:{"title":"책 읽기"})
# - 이번에는 예시 데이터가 아니라, 실제 DB에 저장하는 구조로 구현함
# ------------------------------
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
# task_body: 사용자가 보낸 데이터 요청 본문
# - TaskCreate: 사용자가 보낸 데이터(title만 포함됨)
# - TaskCreateResponse: 응답할 때 포함할 데이터(id 포함)
# - db: FastAPI가 getdb() 함수를 통해 자동으로 주입하는 DB 세션 객체
async def create_task(task_body: task_schema.TaskCreate, db:AsyncSession=Depends(get_db)):
    return await task_crud.create_task(db,task_body)
    # * crud 모듈의 create_task() 함수를 호출하여 실제 DB에 저장함
    # * 저장 후 생성된 할 일(Task)을 반환하며, 그 안에는 id가 포함됨
    #   (예: TaskCreateResponse(id=1,title="책 읽기"))
    #
    # * db: get_db() 함수를 통해 생성된 SQAlchemy 비동기 세션이 자동으로 들어옴
    #   - FastAPI의 Depends를 사용해 '의존성 주입(Dependecy Injection)' 방식으로 처리함
    #   - 테스트 시에는 get_db 함수를 오버라이드해서 가짜 DB나 테스트용 DB를 넣을 수 있ㅇ,ㅁ
    # * 이 구조는 DB 작업(비지니스 로직)은 crud.py에 따로 만들고,
    #   이 함수느 요청 받고 응답하는 역할만 담당하도록 나눠서 구성함
    #   -> 코드가 더 깔끔하고 관리하기 쉬워짐짐

# ------------------------------
# [3] 할 일 수정 기능 (PUT 요청)
# - 경로에 포함된 번호(task_id)에 해당되는 할 일을 수정함
# - 클라이언트가 수정할 내용을 JSON으로 보내면 title을 바꿔주는 역할할
# ------------------------------
@router.put("/tasks/{task_id}",response_model=task_schema.TaskCreateResponse)
# - task_id : URL 경로에 포함된 숫자 (수정 대상 할 일 번호)
# - task_body : 수정할 내용을 담은 요청 본문 (title)

async def update_task(task_id:int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.model_dump())
    # * id는 수정 대상 번호 그대로 사용
    # * 수정된 title과 함께 응답 구조(TaskCReateResponse)로 반환
    # * model_dump()는 title값을 딕셔너리처럼 꺼내주는 함수 (dict() 대신 사용됨)


# ------------------------------
# [4] 할 일 삭제 기능 (DELETE 요청)
# - /tasks/번호 형식으로 요청이 오면 해당 번호의 할 일을 삭제함
# - 이 함수느 아직 DB가 없기 때문에 동작은 하지 않지만 구조만 정의함 
# ------------------------------
@router.delete("/tasks/{task_id}")
# - task_id: 삭제할 일의 번호
# - response_model이 없으므로 별도 응답 내용 없이 처리 가능 (204 No Content)
async def delete_task(task_id: int):
    return
    # * 실제 구현에서는 삭제 후 상태 코드나 메세지를 반환할 수 있음음