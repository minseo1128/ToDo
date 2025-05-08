# ------------------------------
# 파일명: done.py
# 위치: api/schemas/done.py
# 이 파일은 "응답 데이터 형식"을 정의한 곳입니더.
# FastAPI는 사용자의 요청에 대한 응답을 JSON 형식으로 보냅니다.
# 여기서는 완료된 할 잏(Done)에 대한 응답 구조를 정의합니다.
# ------------------------------

from pydantic import BaseModel # 응답 형식을 만들기 위한 클래스


# ------------------------------
# DoneResponse 클래스
# - 할 일이 완료되었을 때 응답에 사용되는 형식입니다.
# - 예: {"id":3}이면, 3번 할 일이 완료 되었음을 의미합니다.
# ------------------------------
class DoneResponse(BaseModel):
    id:int  # 완료된 할 일의 번호
    
    # Config 클래스 설정
    # - from_attributes = True 를 설정하면,
    #   SQLAlchemy 모델 객체를 그대로 사용할 수 있습니다.
    # - Pydantic 2 버전에서는 기존 orm_mode = True 대신
    #   from_attributes=True를 사용해야 경고 없이 동작합니다.
    class Config:
        from_attributes=True
        
        