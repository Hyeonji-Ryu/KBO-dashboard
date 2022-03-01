"""데이터베이스 연결과 세션 형성"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# 첫 실행에서만 Database 생성
ENGINE = create_engine('sqlite:///module/KBO.db',convert_unicode=True)
# 세션 생성: 접속이 끝나더라도 연결 계속 유지 / scoped_session: 동일한 쓰레드에서 세션 충돌 방지 (사람마다 똑같은 세션 객체 저장)
DB_SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

# 데이터베이스와 연결할 가본 클래스 생성
Base = declarative_base()
Base.query = DB_SESSION.query_property()
