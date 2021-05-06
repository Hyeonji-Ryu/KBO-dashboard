"""테이블 생성하거나 업데이트 하는 함수"""
from sqlalchemy import Column, Integer, String, Float
from module.database import Base

# 스코어보드 업데이트 클래스
class scoreboard(Base):
    """테이블 생성하거나 업데이트 하는 클래스 """
    __tablename__ = 'scoreboard'
    idx = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day =  Column(Integer)
    week =  Column(Integer)
    team =  Column(String(3))
    result = Column(Integer)
    i_1 = Column(Integer)
    i_2 = Column(Integer)
    i_3 = Column(Integer)
    i_4 = Column(Integer)
    i_5 = Column(Integer)
    i_6 = Column(Integer)
    i_7 = Column(Integer)
    i_8 = Column(Integer)
    i_9 = Column(Integer)
    i_10 = Column(Integer)
    i_11 = Column(Integer)
    i_12 = Column(Integer)
    R = Column(Integer)
    H = Column(Integer)
    E = Column(Integer)
    B = Column(Integer)
    home = Column(String(3))
    visit = Column(String(3))
    doubleheader = Column(Integer)

    def __init__(self,idx,year,month,day,week,team,result,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,
                 R,H,E,B,home,visit,doubleheader):
        self.idx = idx
        self.year = year
        self.month = month
        self.day = day
        self.week = week
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
        self.R = R
        self.H = H
        self.E = E
        self.B = B
        self.home = home
        self.visit = visit
        self.doubleheader = doubleheader

        def __repr__(self):
            return "<scoreboard('%d', '%d', '%d','%d', '%d', '%s','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',\
                '%d','%d','%d','%d','%s','%s','%d')>" % (self.idx, self.year, self.month, self.day, self.week, self.team,
                    self.result, self.i_1, self.i_2, self.i_3, self.i_4, self.i_5, self.i_6, self.i_7, self.i_8, self.i_9, 
                    self.i_10, self.i_11, self.i_12, self.R, self.H, self.E, self.B, self.home, self.visit, self.doubleheader)

# 타자 테이블 생성 및 업데이트 클래스

class batter(Base):
    """테이블 생성하거나 업데이트 하는 클래스 """
    __tablename__ = 'batter'
    idx = Column(Integer, primary_key=True)
    name = Column(String(20))
    position = Column(String(3))
    team =  Column(String(3))
    doubleheader = Column(Integer)
    home = Column(String(3))
    visit = Column(String(3))
    i_1 = Column(Integer)
    i_2 = Column(Integer)
    i_3 = Column(Integer)
    i_4 = Column(Integer)
    i_5 = Column(Integer)
    i_6 = Column(Integer)
    i_7 = Column(Integer)
    i_8 = Column(Integer)
    i_9 = Column(Integer)
    i_10 = Column(Integer)
    i_11 = Column(Integer)
    i_12 = Column(Integer)
    hit = Column(Integer)
    bat_num = Column(Integer)
    hit_prob = Column(Float)
    hit_get = Column(Integer)
    own_get = Column(Integer)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    week = Column(Integer)
    id = Column(Integer)

    def __init__(self,idx, name, position, team, doubleheader, home, visit, i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,
                 i_9,i_10,i_11,i_12, hit, bat_num,hit_prob,hit_get,own_get,year,month,day,week, id):
        self.idx = idx
        self.name = name
        self.position = position
        self.team = team
        self.doubleheader = doubleheader
        self.home = home
        self.visit = visit
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
        self.hit = hit
        self.bat_num = bat_num
        self.hit_prob = hit_prob 
        self.hit_get = hit_get
        self.own_get = own_get
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.id = id

        def __repr__(self):
            return "<batter('%d', '%s', '%s','%s', '%d', '%s','%s','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',\
                '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')>"  %(self.idx, self.name, self.position, self.team, self.doubleheader, self.home,
                self.visit, self.i_1 , self.i_2 , self.i_3 , self.i_4 , self.i_5, self.i_6, self.i_7, self.i_8, self.i_9, self.i_10,
                self.i_11, self.i_12, self.hit, self.bat_num, self.hit_prob, self.hit_get, self.own_get, self.year, self.month, self.day,
                self.week, self.id)

# 투수 테이블 생성 및 업데이트 클래스

class pitcher(Base):
    """테이블 생성하거나 업데이트 하는 클래스 """
    __tablename__ = 'pitcher'
    idx = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    week = Column(Integer)  
    name = Column(String(20))
    position = Column(String(6))
    team = Column(String(3))
    doubleheader = Column(Integer)
    home = Column(String(3))
    visit = Column(String(3))
    join = Column(Integer)
    inning = Column(Integer) 
    rest = Column(Integer)
    win = Column(Integer)
    lose = Column(Integer)
    draw = Column(Integer)
    save = Column(Integer) 
    hold = Column(Integer)
    strikeout = Column(Integer) 
    deadball= Column(Integer)
    losescore = Column(Integer)
    earnedrun = Column(Integer)
    pitchnum = Column(Integer)
    hited = Column(Integer)
    homerun = Column(Integer) 
    hitnum = Column(Integer)
    hitter = Column(Integer)
    playerid = Column(Integer)
    
    def __init__(self,idx,year,month,day,week,name,position,team,doubleheader,home,visit,join,inning,rest,win,
                 lose,draw,save,hold,strikeout,deadball,losescore,earnedrun,pitchnum,hited,homerun,hitnum, hitter,playerid):
        self.idx = idx
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.name = name
        self.position = position
        self.team = team
        self.doubleheader = doubleheader
        self.home = home
        self.visit = visit
        self.join = join
        self.inning = inning
        self.rest = rest
        self.win = win
        self.lose = lose
        self.draw = draw
        self.save = save
        self.hold = hold
        self.strikeout = strikeout
        self.deadball = deadball
        self.losescore = losescore
        self.earnedrun = earnedrun
        self.pitchnum = pitchnum
        self.hited = hited
        self.homerun = homerun
        self.hitnum = hitnum
        self.hitter = hitter
        self.playerid = playerid

    def __repr__(self):
        return "<pitcher('%d','%d','%d','%d','%d','%s','%s','%s','%d','%s','%s','%d','%d','%d','%d','%d','%d',\
        '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')>"%(self.idx, self.year, self.month, self.day, 
            self.week, self.name, self.position, self.team, self.doubleheader,self.home, self.visit, self.join,
            self.inning, self.rest, self.win, self.lose, self.draw, self.save,self.hold, self.strikeout,
            self.deadball, self.losescore,self.earnedrun,self.pitchnum, self.hited, self.homerun,self.hitnum, self.hitter, self.playerid)