""" 쿼리 보내서 데이터 받아오는 함수들 """
from module.database import ENGINE, DB_SESSION, Base, init_db
from module.model import scoreboard, batter, pitcher
import pandas as pd
import dash_html_components as html
from collections import Counter

# 스코어보드 쿼리 함수
def team_show_tables():
    """ 해당 테이블의 리스트 전부 받아오는 함수 """
    queries = DB_SESSION.query(scoreboard)
    entries = [dict(idx=q.idx, year=q.year, month=q.month, day=q.day, week=q.week, team=q.team, result= q.result,
                    i_1=q.i_1, i_2=q.i_2, i_3=q.i_3, i_4=q.i_4, i_5=q.i_5, i_6=q.i_6, i_7=q.i_7, i_8=q.i_8,
                    i_9=q.i_9, i_10=q.i_10, i_11=q.i_11, i_12=q.i_12, R=q.R, H=q.H, E=q.E, B=q.B, home=q.home,
                    visit=q.visit, doubleheader=q.doubleheader) for q in queries]
    return entries

def team_add_entry(idx,year,month,day,week,team,result,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,
                 R,H,E,B,home,visit,doubleheader):
    """해당 테이블에 레코드 추가하는 함수 """
    temp = scoreboard(idx,year,month,day,week,team,result,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,
                 R,H,E,B,home,visit,doubleheader)
    DB_SESSION.add(temp)
    DB_SESSION.commit()

def team_delete_entry(idx, team):
    """ 헤딩 테이블의 레코드 제거하는 함수 """
    DB_SESSION.query(scoreboard).filter(scoreboard.idx == idx, scoreboard.team == team).delete()
    DB_SESSION.commit()

def batter_show_tables():
    """ 해당 테이블의 리스트 전부 받아오는 함수 """
    queries = DB_SESSION.query(batter)
    entries = [dict(idx=q.idx, name=q.name, position=q.position, team=q.team, doubleheader=q.doubleheader,
                    home=q.home, visit=q.visit, i_1=q.i_1, i_2=q.i_2, i_3=q.i_3, i_4=q.i_4, i_5=q.i_5,
                    i_6=q.i_6, i_7=q.i_7, i_8=q.i_8, i_9=q.i_9, i_10=q.i_10, i_11=q.i_11, i_12=q.i_12,
                    hit=q.hit, bat_num=q.bat_num, hit_prob=q.hit_prob, hit_get=q.hit_get, own_get=q.own_get,
                    year=q.year, month=q.month, day=q.day, week=q.week, id=q.id) for q in queries]
    return entries

def batter_add_entry(idx, name, position, team, doubleheader, home, visit, i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,
              i_11,i_12, hit, bat_num,hit_prob,hit_get,own_get,year,month,day,week, id):
    """해당 테이블에 레코드 추가하는 함수 """
    temp = batter(idx, name, position, team, doubleheader, home, visit, i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,
                 i_9,i_10,i_11,i_12, hit, bat_num,hit_prob,hit_get,own_get,year,month,day,week, id)
    DB_SESSION.add(temp)
    DB_SESSION.commit()

def batter_delete_entry(idx, team):
    """ 헤딩 테이블의 레코드 제거하는 함수 """
    DB_SESSION.query(batter).filter(batter.idx == idx, batter.team == team).delete()
    DB_SESSION.commit()
    
def query_direct(sql_query):
    """sql 쿼리를 직접 보내서 데이터 가져오는 함수"""
    result = DB_SESSION.execute(sql_query)
    get_data = result.fetchall() # type: list
    DB_SESSION.close()
    return get_data

def pitcher_add_entry(idx,year,month,day,week,name,position,team,doubleheader,home,visit,join,inning,rest,win,
                 lose,draw,save,hold,strikeout,deadball,losescore,earnedrun,pitchnum,hited,homerun,hitnum,hitter,playerid):
    """해당 테이블에 레코드 추가하는 함수 """
    temp = pitcher(idx,year,month,day,week,name,position,team,doubleheader,home,visit,join,inning,rest,win,
                 lose,draw,save,hold,strikeout,deadball,losescore,earnedrun,pitchnum,hited,homerun,hitnum,hitter,playerid)
    db_session.add(temp)
    db_session.commit()

# DB 처리하는 함수

def count_year():
    data = query_direct("SELECT DISTINCT year FROM scoreboard")
    return  sorted([year[0] for year in data],reverse=True)

## 팀 대시보드 DB 처리 함수

def team_win_table(team_name):
    sql_lose = f"SELECT year, count(result) FROM scoreboard WHERE result = -1 and team = '{team_name}' GROUP BY year" 
    sql_win = f"SELECT count(result) FROM scoreboard WHERE result = 1 and team = '{team_name}' GROUP BY year" 
    lose = query_direct(sql_lose)
    win = query_direct(sql_win) 
    prop = []
    year = []
    pred = []
    for i in range(len(win)):
        prop.append(win[i][0]/(lose[i][1]+win[i][0]))
        year.append(lose[i][0])
        pred.append(win[i][0]**1.83/(lose[i][1]**1.83+win[i][0]**1.83))
    return year, prop, pred

def month_win_prop(team_name):
    sql = f"SELECT month,count(result) FROM scoreboard WHERE team = '{team_name}' GROUP BY month" 
    sql_win = f"SELECT month,count(result) FROM scoreboard WHERE team = '{team_name}' and result = 1 GROUP BY month" 
    monthly = query_direct(sql)
    win_monthly = query_direct(sql_win)
    prop = []
    for i in range(len(monthly)):
        prop.append(win_monthly[i][1]/monthly[i][1])
    return prop

def home_visit_prop(team_name):
    sql_home = f"SELECT result,count(result) FROM scoreboard WHERE team = '{team_name}' and home ='{team_name}' GROUP BY result" 
    sql_visit = f"SELECT result,count(result) FROM scoreboard WHERE team = '{team_name}' and visit ='{team_name}' GROUP BY result" 
    home = query_direct(sql_home)
    visit = query_direct(sql_visit)
    home_df = pd.DataFrame(home, columns = ['result','score'])
    visit_df = pd.DataFrame(visit, columns = ['result','score'])
    if len(home)>0:
        num = (home_df['score'][2]/sum(home_df['score']))-(visit_df['score'][2]/sum(visit_df['score']))
    else: num = 'None'
    return home_df, visit_df, num

def team_win_porb(team_name):
    sql_home = f"SELECT visit, result FROM scoreboard WHERE team = '{team_name}' and home = '{team_name}'" 
    sql_visit = f"SELECT home, result FROM scoreboard WHERE team = '{team_name}' and visit = '{team_name}'" 
    home_= query_direct(sql_home)
    visit_= query_direct(sql_visit)
    home= pd.DataFrame(home_, columns=['team','score'])
    visit= pd.DataFrame(visit_, columns=['team','score'])
    total_a= Counter(dict(home['team'].value_counts()))
    total_b= Counter(dict(visit['team'].value_counts()))
    win_a= Counter(dict(home[home.score == 1]['team'].value_counts()))
    win_b= Counter(dict(visit[visit.score == 1]['team'].value_counts()))
    total= total_a + total_b
    win=win_a+win_b
    if len(total) != 0:
        prop=[(team,round(win[team]/total[team],3)) for team in total.keys()]
    else:
        prop =[('SK',0.0) ,('기아',0.0),('두산',0.0),('한화',0.0),('LG',0.0),('삼성',0.0),('키움',0.0),('롯데',0.0),('NC',0.0),('KT',0.0)]
    prop = pd.DataFrame(prop,columns=['team','prop'])
    frame= [('기아', 35.16827113473779, 126.88899043224903),('KT', 37.29786570544838, 127.01131452674122),
            ('LG', 37.51506611640175, 127.07313385765605),('두산', 37.51255338179348, 127.07188253458176),('NC', 35.222642265641134, 128.58274545553056),
            ('SK', 37.4362522604058, 126.6890951402365),('롯데', 35.19519530402531, 129.06093468251407),('삼성', 35.84102380422949, 128.68123826903627),
            ('키움', 37.49834690696769, 126.8672292844178),('한화', 36.31744463309478, 127.42853811137499)]
    df = pd.DataFrame(frame,columns = ['team','lat','lon'])
    own= df[df.team == team_name].index
    df= df.drop(own)
    df = pd.merge(df,prop,how='outer',on='team')
    return df

## 타자 대시보드 DB 처리 함수

def batter_list(year,team):

    data = DB_SESSION.query(batter.name).filter(batter.year == year, batter.team == team).group_by(batter.name).all()
    DB_SESSION.close()
    batter_name = []
    for i in range(len(data)):
            temp = data[i][0]
            batter_name.append(temp)
    return batter_name

def batter_names():

    sql = "SELECT DISTINCT name FROM batter WHERE year = 2020;" 
    batter_name = query_direct(sql)
    temp = [batter_name[i][0] for i in range(len(batter_name))]
    return temp

def batter_yearly_base(name):
    # 전처리
    scores = [(0,0,0,0,0,0)]
    sql = f"SELECT year,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,hit,bat_num FROM batter WHERE name = '{name}'"
    data = query_direct(sql)
    temp = pd.DataFrame(data,columns=['year','i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9','i_10','i_11','i_12','hit','bat_num'])
    for year in temp['year'].unique():
        score_list =Counter({})
        for num in ['i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9','i_10','i_11','i_12']:
            lis=Counter(dict(temp[temp.year == year][num].value_counts()))
            score_list += lis
        # 값 계산
        try:
            AVG= round(sum(temp[temp.year == year]['hit'])/sum(temp[temp.year == year]['bat_num']),3)
            obp_a= (score_list[3100]+score_list[3000])
            obp_b= (score_list[5000]+score_list[5001]+score_list[5002]+score_list[5003]+score_list[5004]+score_list[5005])
            OBP= round((sum(temp[temp.year == year]['hit'])+obp_a)/(obp_a+obp_b+sum(temp[temp.year == year]['bat_num'])),3)
            one= [score_list[num] for num in range(1000,1030)]
            two= [score_list[num] for num in range(1100,1122)]
            three= [score_list[num] for num in range(1200,1206)]
            homerun = [score_list[num] for num in range(1300,1305)]
            SLG= round((sum(one)+2*sum(two)+3*sum(three)+4*sum(homerun))/sum(temp[temp.year == year]['bat_num']),3)
            ISO= round(SLG-AVG,3)
            EOBP= round(OBP-AVG,3)
        except:
            AVG, OBP, SLG, ISO, EOBP = 0,0,0,0,0
        scores.append((year, AVG, OBP, SLG, ISO, EOBP))
    return scores

def daily_hit_prob(name):
    sql = f"SELECT month,day,hit_prob FROM batter WHERE name = '{name}'"
    prob = query_direct(sql)
    df = pd.DataFrame(prob,columns=['month','day','value'],dtype = str)
    df['date'] = df[['month', 'day']].agg('.'.join, axis=1)
    return df

## 투수 대시보드 DB 처리 함수

def pitcher_list(year,team):

    data = DB_SESSION.query(pitcher.name).filter(pitcher.year == year, pitcher.team == team).group_by(pitcher.name).all()
    DB_SESSION.close()
    pitcher_name = []
    for i in range(len(data)):
            temp = data[i][0]
            pitcher_name.append(temp)
    return pitcher_name

def pitcher_names():

    sql = "SELECT DISTINCT name FROM pitcher WHERE year = 2020;" 
    pitcher_name = query_direct(sql)
    temp = [pitcher_name[i][0] for i in range(len(pitcher_name))]
    return temp

def pitcher_yearly_base(player_name):
    sql = f"SELECT year, sum(inning), sum(rest), sum(earnedrun), sum(strikeout),sum(homerun), sum(hited), sum(hitnum), sum(deadball), sum(losescore) FROM pitcher WHERE name = '{player_name}' GROUP BY year"
    name = query_direct(sql)
    temp = pd.DataFrame(name, columns=['year','inning', 'rest', 'earnedrun', 'strikeout','homerun', 'hited', 'hitnum', 'deadball','losescore'],dtype='int64')
    scores = [(0,0,0,0,0,0)]
    for year in temp['year']:
        inning = temp[temp.year==year]['inning']+temp[temp.year==year]['rest']/3
        ERA = float(round((9*temp[temp.year==year]['earnedrun'])/inning,3))
        FIP = float(round(((13*temp[temp.year==year]['homerun'] + 3*temp[temp.year==year]['deadball']-2*temp[temp.year==year]['strikeout'])/inning + 3.2),3))
        RA9 = float(round((temp[temp.year==year]['losescore']/inning)*9,3))
        OBP = float(round((temp[temp.year==year]['hited']+temp[temp.year==year]['deadball'])/(temp[temp.year==year]['hitnum']+temp[temp.year==year]['deadball']),3))
        AVG = float(round((temp[temp.year==year]['hited']/temp[temp.year==year]['hitnum']),3))
        scores.append((year, AVG, OBP, RA9, ERA, FIP))
    df= pd.DataFrame(scores[1:], columns=['YEAR','AVG','OBP','RA9','ERA','FIP'])
    df.replace(float('inf'), 0, inplace=True)
    df= df.fillna(0)
    return scores, df

def pitcher_prop(player_name):
    sql = f"SELECT year,month,sum(hited),sum(hitnum),sum(deadball) FROM pitcher WHERE name = '{player_name}' GROUP BY year, month"
    name = query_direct(sql)
    temp = pd.DataFrame(name, columns=['year','month','hited', 'hitnum','deadball'],dtype=str)
    temp['date'] = temp[['year','month']].agg('-'.join, axis=1)
    temp['AVG'] = round(temp['hited'].astype(float)/temp['hitnum'].astype(float),3)
    temp['OBP'] = round((temp['hited'].astype(float)+temp['deadball'].astype(float))/(temp['hitnum'].astype(float)+temp['deadball'].astype(float)),3)
    return temp