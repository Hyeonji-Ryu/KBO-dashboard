"""테이블 생성하거나 업데이트 하는 함수"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint
from module.database import Base
from sqlalchemy.dialects import mysql


# 스코어보드 (업데이트 완료)

class scoreboard(Base):
    """테이블 생성하거나 업데이트 하는 클래스 """
    __tablename__ = 'scoreboard'
    idx = Column(mysql.BIGINT(11), primary_key=True,autoincrement=False)
    team = Column(String(4))
    result = Column(mysql.INTEGER(1))
    i_1 = Column(mysql.INTEGER(2))
    i_2 = Column(mysql.INTEGER(2))
    i_3 = Column(mysql.INTEGER(2))
    i_4 = Column(mysql.INTEGER(2))
    i_5 = Column(mysql.INTEGER(2))
    i_6 = Column(mysql.INTEGER(2))
    i_7 = Column(mysql.INTEGER(2))
    i_8 = Column(mysql.INTEGER(2))
    i_9 = Column(mysql.INTEGER(2))
    i_10 = Column(mysql.INTEGER(2))
    i_11 = Column(mysql.INTEGER(2))
    i_12 = Column(mysql.INTEGER(2))
    i_13 = Column(mysql.INTEGER(2))
    i_14 = Column(mysql.INTEGER(2))
    i_15 = Column(mysql.INTEGER(2))
    i_16 = Column(mysql.INTEGER(2))
    i_17 = Column(mysql.INTEGER(2))
    i_18 = Column(mysql.INTEGER(2))
    r = Column(mysql.INTEGER(2))
    h = Column(mysql.INTEGER(2))
    e = Column(mysql.INTEGER(2))
    b = Column(mysql.INTEGER(2))
    year = Column(mysql.INTEGER(4))
    month = Column(mysql.INTEGER(2))
    day =  Column(mysql.INTEGER(2))
    week =  Column(mysql.INTEGER(1))
    home = Column(String(4))
    away = Column(String(4))
    dbheader = Column(mysql.INTEGER(1))
    place = Column(String(3))
    audience = Column(mysql.INTEGER(6))
    starttime = Column(String(5))
    endtime = Column(String(5))
    gametime = Column(String(5))

    def __init__(self,idx,team,result,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,i_13,
                 i_14,i_15,i_16,i_17,i_18,r,h,e,b,year,month,day,week,home,away,dbheader,place,audience,
                 starttime,endtime,gametime):
        self.idx = idx
        self.team = team
        self.result = result
        self.i_1 = i_1
        self.i_2 = i_2
        self.i_3 = i_3
        self.i_4 = i_4
        self.i_5 = i_5
        self.i_6 = i_6
        self.i_7 = i_7
        self.i_8 = i_8
        self.i_9 = i_9
        self.i_10 = i_10
        self.i_11 = i_11
        self.i_12 = i_12
        self.i_13 = i_13
        self.i_14 = i_14
        self.i_15 = i_15
        self.i_16 = i_16
        self.i_17 = i_17
        self.i_18 = i_18
        self.r = r
        self.h = h
        self.e = e
        self.b = b
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.home = home
        self.away = away
        self.dbheader = dbheader
        self.place = place
        self.audience = audience
        self.starttime = starttime
        self.endtime = endtime
        self.gametime = gametime
        
        def __repr__(self):
            return "<scoreboard('%d', '%s', '%d','%d', '%d', '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d'\
        '%d','%d','%d','%d','%d','%d','%d','%d','%s','%s','%d','%s','%d','%s','%s','%s')>" % (self.idx,self.team,self.result, self.i_1, self.i_2, self.i_3, self.i_4, self.i_5, self.i_6, self.i_7, self.i_8,
                                                         self.i_9, self.i_10, self.i_11, self.i_12, self.i_13, self.i_14, self.i_15, self.i_16, self.i_17, self.i_18,
                                                         self.r, self.h, self.e, self.b,self.year, self.month, self.day, self.week, self.home, self.away, self.dbheader,)


# 타자 (업데이트 완료)

class batter(Base):
    """테이블 생성하거나 업데이트 하는 클래스 """
    __tablename__ = "batter"
    __table_args__ = {'extend_existing': True}
    idx = Column(mysql.INTEGER(11), ForeignKey('scoreboard.idx'), primary_key = True)
    name = Column(String(8))
    team = Column(String(4))
    position = Column(String(2))
    i_1 = Column(mysql.INTEGER(8))
    i_2 = Column(mysql.INTEGER(8))
    i_3 = Column(mysql.INTEGER(8))
    i_4 = Column(mysql.INTEGER(8))
    i_5 = Column(mysql.INTEGER(8))
    i_6 = Column(mysql.INTEGER(8))
    i_7 = Column(mysql.INTEGER(8))
    i_8 = Column(mysql.INTEGER(8))
    i_9 = Column(mysql.INTEGER(8))
    i_10 = Column(mysql.INTEGER(8))
    i_11 = Column(mysql.INTEGER(8))
    i_12 = Column(mysql.INTEGER(8))
    i_13 = Column(mysql.INTEGER(8))
    i_14 = Column(mysql.INTEGER(8))
    i_15 = Column(mysql.INTEGER(8))
    i_16 = Column(mysql.INTEGER(8))
    i_17 = Column(mysql.INTEGER(8))
    i_18 = Column(mysql.INTEGER(8))
    hit = Column(mysql.INTEGER(2))
    bat_num = Column(mysql.INTEGER(2))
    hit_get = Column(mysql.INTEGER(2))
    own_get = Column(mysql.INTEGER(2))

    def __init__(self,idx,name,team,position,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,
                 i_13,i_14,i_15,i_16,i_17,i_18,hit,bat_num,hit_get,own_get):
        self.idx = idx
        self.name = name
        self.team = team
        self.position = position
        self.i_1 = i_1
        self.i_2 = i_2
        self.i_3 = i_3
        self.i_4 = i_4
        self.i_5 = i_5
        self.i_6 = i_6
        self.i_7 = i_7
        self.i_8 = i_8
        self.i_9 = i_9
        self.i_10 = i_10
        self.i_11 = i_11
        self.i_12 = i_12
        self.i_13 = i_13
        self.i_14 = i_14
        self.i_15 = i_15
        self.i_16 = i_16
        self.i_17 = i_17
        self.i_18 = i_18
        self.hit = hit
        self.bat_num = bat_num
        self.hit_get = hit_get
        self.own_get = own_get

        def __repr__(self):
            return "<batter('%d', '%s', '%s','%s', '%d', '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',\
                '%d','%d','%d','%d','%d','%d','%d')>"  %(self.idx, self.name,self.team, self.position, self.i_1, self.i_2, self.i_3, self.i_4,
                                                         self.i_5, self.i_6, self.i_7, self.i_8, self.i_9, self.i_10, self.i_11, self.i_12,
                                                         self.i_13, self.i_14,self.i_15, self.i_16, self.i_17, self.i_18, self.hit,
                                                         self.bat_num, self.hit_get, self.own_get)


# 투수 업데이트 완료

class pitcher(Base):
    """테이블 생성하거나 업데이트 하는 클래스 """
    __tablename__ = "pitcher"
    __table_args__ = {'extend_existing': True}
    idx = Column(mysql.INTEGER(11), ForeignKey('scoreboard.idx'), primary_key = True)
    name = Column(String(8))
    team = Column(String(4))
    mound = Column(mysql.TINYINT(1))
    inning = Column(mysql.INTEGER(3))
    result = Column(String(1))
    strikeout = Column(mysql.INTEGER(2))
    dead4ball = Column(mysql.INTEGER(2))
    losescore = Column(mysql.INTEGER(2))
    earnedrun = Column(mysql.INTEGER(2))
    pitchnum = Column(mysql.INTEGER(3))
    hitted = Column(mysql.INTEGER(2))
    homerun = Column(mysql.INTEGER(2))
    battednum = Column(mysql.INTEGER(2))
    batternum = Column(mysql.INTEGER(2))

    def __init__(self,idx,name,team,mound,inning,result,strikeout,dead4ball,losescore,earnedrun,
                 pitchnum,hitted,homerun,battednum,batternum):
        self.idx = idx
        self.name = name
        self.team = team
        self.mound = mound
        self.inning = inning
        self.result = result
        self.strikeout = strikeout
        self.dead4ball = dead4ball
        self.losescore = losescore
        self.earnedrun = earnedrun
        self.pitchnum = pitchnum
        self.hitted = hitted
        self.homerun = homerun
        self.battednum = battednum
        self.batternum = batternum

        def __repr__(self):
            return "<pitcher('%d','%s','%s','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d','%d','%d')>" %(self.idx,self.name,self.team,self.mound,self.inning,
                                                         self.result,self.strikeout,self.dead4ball,self.losescore,self.earnedrun,self.pitchnum,
                                                         self.hitted,self.homerun,self.battednum,self.batternum)
