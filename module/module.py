""" 쿼리 보내서 데이터 받아오는 함수들 """
from module.database import ENGINE, DB_SESSION, Base
from module.model import scoreboard, batter, pitcher
import pandas as pd
import dash_html_components as html
from collections import Counter

# 모든 대시보드에서 사용하는 함수

def query_direct(sql_query):
    """sql 쿼리를 직접 보내서 데이터 가져오는 함수"""
    result = DB_SESSION.execute(sql_query)
    get_data = result.fetchall() # type: list
    DB_SESSION.close()
    return get_data

def count_year():
    data = query_direct("SELECT DISTINCT year FROM scoreboard")
    return  sorted([year[0] for year in data],reverse=True)

def get_team_name(year):
    data = query_direct(f"SELECT DISTINCT team FROM scoreboard where year ='{year}'")
    return  sorted([name[0] for name in data],reverse=True)

# 스코어보드 전용 함수

def team_win_table(team_name):
    """각 팀의 승률을 가져오는 함수: 히어로즈의 경우 스폰서만 계속 변경되었기에 같은 팀으로 설정
       Output: tuple(년도(list), 실제승률(list), 기대승률(list))
    """
    if team_name == "키움":
        sql_lose = f"SELECT year, count(result) FROM scoreboard WHERE result = -1 and team IN ('키움','넥센','우리','히어로즈') GROUP BY year" 
        sql_win = f"SELECT count(result) FROM scoreboard WHERE result = 1 and team IN ('키움','넥센','우리','히어로즈') GROUP BY year" 
    else:
        sql_lose = f"SELECT year, count(result) FROM scoreboard WHERE result = -1 and team = '{team_name}' GROUP BY year" 
        sql_win = f"SELECT count(result) FROM scoreboard WHERE result = 1 and team = '{team_name}' GROUP BY year" 
    lose = query_direct(sql_lose)
    win = query_direct(sql_win)
    year = []
    # 실제 승률
    prop = []
    # 기대 승률
    pred = []
    for i in range(len(win)):
        prop.append(win[i][0]/(lose[i][1]+win[i][0]))
        year.append(lose[i][0])
        pred.append(win[i][0]**1.83/(lose[i][1]**1.83+win[i][0]**1.83))
    return year, prop, pred

def month_win_prob(team_name):
    """월별 승률을 가져오는 함수: 히어로즈의 경우 스폰서만 계속 변경되었기에 같은 팀으로 설정
       Output: tuple(월(list),월별승률(list))
    """
    if team_name == "키움":
        sql = f"SELECT month,count(result) FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') GROUP BY month" 
        sql_win = f"SELECT month,count(result) FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') and result = 1 GROUP BY month"
    else:
        sql = f"SELECT month,count(result) FROM scoreboard WHERE team = '{team_name}' GROUP BY month" 
        sql_win = f"SELECT month,count(result) FROM scoreboard WHERE team = '{team_name}' and result = 1 GROUP BY month" 
    monthly = query_direct(sql)
    win_monthly = query_direct(sql_win)
    month = []
    prop = []
    for i in range(len(monthly)):
        month.append(win_monthly[i][0])
        prop.append(win_monthly[i][1]/monthly[i][1])
    return month,prop

def home_visit_prob(team_name):
    """홈경기, 원정경기에 따른 승률을 계산하는 함수: 히어로즈의 경우 스폰서만 계속 변경되었기에 같은 팀으로 설정
       Output: 홈경기 결과, 원정경기 결과, 승률의 차
    """
    if team_name == "키움":
        sql_home = f"SELECT result,count(result) FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') and home IN ('키움','넥센','우리','히어로즈') GROUP BY result" 
        sql_visit = f"SELECT result,count(result) FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') and away IN ('키움','넥센','우리','히어로즈') GROUP BY result"
    else:
        sql_home = f"SELECT result,count(result) FROM scoreboard WHERE team = '{team_name}' and home ='{team_name}' GROUP BY result" 
        sql_visit = f"SELECT result,count(result) FROM scoreboard WHERE team = '{team_name}' and away ='{team_name}' GROUP BY result" 
    home = query_direct(sql_home)
    visit = query_direct(sql_visit)
    home_df = pd.DataFrame(home, columns = ['result','score'])
    visit_df = pd.DataFrame(visit, columns = ['result','score'])
    if len(home)>0:
        num = (home_df['score'][2]/sum(home_df['score']))-(visit_df['score'][2]/sum(visit_df['score']))
    else: num = 'None'
    return home_df, visit_df, num

def team_win_prob(team_name):
    """구단 별 1:1 승률 값을 가져오는 함수: 히어로즈의 경우 스폰서만 계속 변경되었기에 같은 팀으로 설정
       Output: 팀이름,구장위치,승률
    """
    if team_name == "키움":
        sql_home = f"SELECT away, result FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') and home IN ('키움','넥센','우리','히어로즈')" 
        sql_visit = f"SELECT home, result FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') and away IN ('키움','넥센','우리','히어로즈')" 
    else:  
        sql_home = f"SELECT away, result FROM scoreboard WHERE team = '{team_name}' and home = '{team_name}'" 
        sql_visit = f"SELECT home, result FROM scoreboard WHERE team = '{team_name}' and away = '{team_name}'" 
    
    home_= query_direct(sql_home)
    visit_= query_direct(sql_visit)
    home= pd.DataFrame(home_, columns=['team','score'])
    visit= pd.DataFrame(visit_, columns=['team','score'])
    # 히어로즈 이전 스폰서들 키움으로 변환
    home["team"] = home["team"].replace(["히어로즈","우리","넥센"],"키움")
    visit["team"] = visit["team"].replace(["히어로즈","우리","넥센"],"키움")
    # 1:1 승률 계산
    total_a= Counter(dict(home['team'].value_counts()))
    total_b= Counter(dict(visit['team'].value_counts()))
    win_a= Counter(dict(home[home.score == 1]['team'].value_counts()))
    win_b= Counter(dict(visit[visit.score == 1]['team'].value_counts()))
    total= total_a + total_b
    win=win_a+win_b
    if len(total) != 0:
        prop=[(team,round(win[team]/total[team],3)) for team in total.keys()]
    else:
        prop =[('SK',0.0) ,('KIA',0.0),('두산',0.0),('한화',0.0),('LG',0.0),('삼성',0.0),('키움',0.0),('롯데',0.0),('NC',0.0),('KT',0.0),('SSG',0.0)]
    prop = pd.DataFrame(prop,columns=['team','prop'])
    ## 구장 별 맵 위도,경도 위치
    frame= [('KIA', 35.16827113473779, 126.88899043224903),('KT', 37.29786570544838, 127.01131452674122),
            ('LG', 37.51506611640175, 127.07313385765605),('두산', 37.51255338179348, 127.07188253458176),('NC', 35.222642265641134, 128.58274545553056),
            ('SK', 37.4362522604058, 126.6890951402365),('롯데', 35.19519530402531, 129.06093468251407),('삼성', 35.84102380422949, 128.68123826903627),
            ('키움', 37.49834690696769, 126.8672292844178),('한화', 36.31744463309478, 127.42853811137499),('SSG', 37.4362522604058, 126.6890951402365),]
    df = pd.DataFrame(frame,columns = ['team','lat','lon'])
    df = pd.merge(df,prop,how='inner',on='team')
    return df

# 타자 전용 함수

def batter_list(year,team):
    """년도별 팀에 속한 선수들의 이름을 가져오는 함수: 히어로즈의 경우 스폰서만 계속 변경되었기에 같은 팀으로 설정
       Output: 선수이름(list)
    """
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT DISTINCT batter.name FROM batter INNER JOIN scoreboard ON batter.idx = scoreboard.idx WHERE scoreboard.year = '{year}' and batter.team IN ('키움','넥센','우리','히어로즈')" 
    else:
        sql = f"SELECT DISTINCT batter.name FROM batter INNER JOIN scoreboard ON batter.idx = scoreboard.idx WHERE scoreboard.year = '{year}' and batter.team = '{team}'"
    batter_name = query_direct(sql)
    temp = [batter_name[i][0] for i in range(len(batter_name))]
    return temp

def daily_hit_prob(team,name):
    
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT scoreboard.month, scoreboard.day, batter.hit ,batter.bat_num FROM batter INNER JOIN scoreboard ON batter.idx = scoreboard.idx where batter.name = '{name}' and batter.team IN ('키움','넥센','우리','히어로즈')"
    else:
        sql = f"SELECT scoreboard.month, scoreboard.day, batter.hit ,batter.bat_num FROM batter INNER JOIN scoreboard ON batter.idx = scoreboard.idx where batter.name = '{name}' and batter.team = '{team}'"
    prob = query_direct(sql)
    df = pd.DataFrame(prob,columns=['month','day','hit','num'])
    df = df.astype({'month':str,'day':str,'hit':int,'num':int})
    df['date'] = df[['month', 'day']].agg('.'.join, axis=1)
    df["value"] = df['hit']/df['num']
    return df

def batter_yearly_base(team,name):
    """타자 이닝 점수 분석 후 결과를 가져오는 함수
       Output: AVG, OBP, SLG, ISO, EOBP
       Explanation:
        - AVG: 평균타율
        - OBP: 출루율
        - SLG: 장타율
        - ISO: 순장타율
        - EOBP: 순출루율
    """
    # 전처리
    scores = [(0,0,0,0,0,0)]
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT scoreboard.year,batter.i_1,batter.i_2,batter.i_3,batter.i_4,batter.i_5,batter.i_6,batter.i_7,batter.i_8,batter.i_9,batter.i_10\
            ,batter.i_11,batter.i_12,batter.i_13,batter.i_14,batter.i_15,batter.i_16,batter.i_17,batter.i_18,batter.hit,batter.bat_num FROM batter INNER JOIN scoreboard\
            ON batter.idx = scoreboard.idx WHERE batter.name = '{name}' and batter.team IN ('키움','넥센','우리','히어로즈')"
    else:
        sql = f"SELECT scoreboard.year,batter.i_1,batter.i_2,batter.i_3,batter.i_4,batter.i_5,batter.i_6,batter.i_7,batter.i_8,batter.i_9,batter.i_10\
            ,batter.i_11,batter.i_12,batter.i_13,batter.i_14,batter.i_15,batter.i_16,batter.i_17,batter.i_18,batter.hit,batter.bat_num FROM batter INNER JOIN scoreboard\
            ON batter.idx = scoreboard.idx WHERE batter.name = '{name}' and batter.team = '{team}'"
    data = query_direct(sql)
    temp = pd.DataFrame(data,columns=['year','i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9','i_10','i_11','i_12','i_13','i_14','i_15','i_16','i_17','i_18','hit','bat_num'])
    for year in temp['year'].unique():
        score_list =Counter({})
        for num in ['i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9','i_10','i_11','i_12','i_13','i_14','i_15','i_16','i_17','i_18']:
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

# 투수 전용 함수

def pitcher_list(year,team):
    """년도별 팀에 속한 선수들의 이름을 가져오는 함수: 히어로즈의 경우 스폰서만 계속 변경되었기에 같은 팀으로 설정
       Output: 선수이름(list)
    """
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT DISTINCT pitcher.name FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE scoreboard.year = '{year}' and pitcher.team IN ('키움','넥센','우리','히어로즈')" 
    else:
        sql = f"SELECT DISTINCT pitcher.name FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE scoreboard.year = '{year}' and pitcher.team = '{team}'"
    pitcher_name = query_direct(sql)
    temp = [pitcher_name[i][0] for i in range(len(pitcher_name))]
    return temp

def pitcher_prop(team,name):
    """년도-월별 투수 분석 결과를 가져오는 함수
       Output: AVG, OBP
       Explanation:
        - AVG: 피타율
        - OBP: 피출루율
    """
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT scoreboard.year, scoreboard.month, sum(pitcher.hitted),sum(pitcher.pitchnum),sum(pitcher.dead4ball) FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{name}' and pitcher.team IN ('키움','넥센','우리','히어로즈') GROUP BY scoreboard.year, scoreboard.month"
    else:
        sql = f"SELECT scoreboard.year, scoreboard.month, sum(pitcher.hitted),sum(pitcher.pitchnum),sum(pitcher.dead4ball) FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{name}' and pitcher.team = '{team}' GROUP BY scoreboard.year, scoreboard.month"
    name = query_direct(sql)
    temp = pd.DataFrame(name, columns=['year','month','hitted', 'pitchnum','dead4ball'],dtype=str)
    temp['date'] = temp[['year','month']].agg('-'.join, axis=1)
    temp['AVG'] = round(temp['hitted'].astype(float)/temp['pitchnum'].astype(float),3)
    temp['OBP'] = round((temp['hitted'].astype(float)+temp['dead4ball'].astype(float))/(temp['pitchnum'].astype(float)+temp['dead4ball'].astype(float)),3)
    return temp

def pitcher_inning_calculator(team,player_name):
    """특정 투수의 년도 별 이닝 수를 도출하는 함수
    """
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT scoreboard.year,pitcher.inning FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{player_name}' and pitcher.team IN ('키움','넥센','우리','히어로즈')"
    else:
        sql = f"SELECT scoreboard.year,pitcher.inning FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{player_name}' and pitcher.team = '{team}'"
    data = query_direct(sql)
    output = {}
    # 년도별 이닝과 나머지 계산
    for year, inning in data:
        if year not in output.keys():
            output[year] = [0,0]
        if len(str(inning)) == 1:
            output[year][1] += int(str(inning)[-1:])
        else:
            output[year][0] += int(str(inning)[:-1])
            output[year][1] += int(str(inning)[-1:])
    return output

def pitcher_yearly_base(team, player_name):
    """특정 투수의 분석 데이터를 가져오는 함수
       Output:
       Explanation:
        - ERA: 평균자책점
        - FIP: 수비무관투구
        - RA9: 평균실점
        - OBP: 피출루율
        - AVP: 피타율
    """
    if team in ['키움','넥센','우리','히어로즈']:
        sql = f"SELECT scoreboard.year,sum(pitcher.earnedrun),sum(pitcher.strikeout),sum(pitcher.homerun), sum(pitcher.hitted), sum(pitcher.pitchnum), sum(pitcher.dead4ball), sum(pitcher.losescore) FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{player_name}' and pitcher.team IN ('키움','넥센','우리','히어로즈') GROUP BY year"
    else:
        sql = f"SELECT scoreboard.year,sum(pitcher.earnedrun),sum(pitcher.strikeout),sum(pitcher.homerun), sum(pitcher.hitted), sum(pitcher.pitchnum), sum(pitcher.dead4ball), sum(pitcher.losescore) FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{player_name}' and pitcher.team = '{team}' GROUP BY year"
    info = query_direct(sql)
    innings = pitcher_inning_calculator(team, player_name)
    temp = pd.DataFrame(info, columns=['year','earnedrun', 'strikeout','homerun', 'hitted', 'pitchnum', 'dead4ball','losescore'],dtype='int64')
    scores = [(0,0,0,0,0,0)]
    for year in temp['year']:
        inning = innings[year][0]+round(innings[year][1]/3,2)
        ERA = float(round((9*temp[temp.year==year]['earnedrun'])/inning,3))
        FIP = float(round(((13*temp[temp.year==year]['homerun'] + 3*temp[temp.year==year]['dead4ball']-2*temp[temp.year==year]['strikeout'])/inning + 3.2),3))
        RA9 = float(round((temp[temp.year==year]['losescore']/inning)*9,3))
        OBP = float(round((temp[temp.year==year]['hitted']+temp[temp.year==year]['dead4ball'])/(temp[temp.year==year]['pitchnum']+temp[temp.year==year]['dead4ball']),3))
        AVG = float(round((temp[temp.year==year]['hitted']/temp[temp.year==year]['pitchnum']),3))
        scores.append((year, AVG, OBP, RA9, ERA, FIP))
    df= pd.DataFrame(scores[1:], columns=['YEAR','AVG','OBP','RA9','ERA','FIP'])
    df.replace(float('inf'), 0, inplace=True)
    df= df.fillna(0)
    return scores, df

# 비교 대시보드

def batter_names():
    sql = "SELECT DISTINCT name FROM batter;" 
    batter_name = query_direct(sql)
    return [name[0] for name in batter_name]

def pitcher_names():
    sql = "SELECT DISTINCT name FROM pitcher;" 
    pitcher_name = query_direct(sql)
    return [name[0] for name in pitcher_name]

def c_batter_yearly_base(name):
    """타자 이닝 점수 분석 후 결과를 가져오는 함수
       Output: AVG, OBP, SLG, ISO, EOBP
       Explanation:
        - AVG: 평균타율
        - OBP: 출루율
        - SLG: 장타율
        - ISO: 순장타율
        - EOBP: 순출루율
    """
    # 전처리
    scores = [(0,0,0,0,0,0)]
    sql = f"SELECT scoreboard.year,batter.i_1,batter.i_2,batter.i_3,batter.i_4,batter.i_5,batter.i_6,batter.i_7,batter.i_8,batter.i_9,batter.i_10\
        ,batter.i_11,batter.i_12,batter.i_13,batter.i_14,batter.i_15,batter.i_16,batter.i_17,batter.i_18,batter.hit,batter.bat_num FROM batter INNER JOIN scoreboard\
        ON batter.idx = scoreboard.idx WHERE batter.name = '{name}'"
    data = query_direct(sql)
    temp = pd.DataFrame(data,columns=['year','i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9','i_10','i_11','i_12','i_13','i_14','i_15','i_16','i_17','i_18','hit','bat_num'])
    for year in temp['year'].unique():
        score_list =Counter({})
        for num in ['i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9','i_10','i_11','i_12','i_13','i_14','i_15','i_16','i_17','i_18']:
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

def c_pitcher_yearly_base(player_name):
    """특정 투수의 분석 데이터를 가져오는 함수
       Output:
       Explanation:
        - ERA: 평균자책점
        - FIP: 수비무관투구
        - RA9: 평균실점
        - OBP: 피출루율
        - AVP: 피타율
    """
    sql = f"SELECT scoreboard.year,sum(pitcher.earnedrun),sum(pitcher.strikeout),sum(pitcher.homerun), sum(pitcher.hitted), sum(pitcher.pitchnum), sum(pitcher.dead4ball), sum(pitcher.losescore) FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{player_name}' GROUP BY year"
    info = query_direct(sql)
    innings = c_pitcher_inning_calculator(player_name)
    temp = pd.DataFrame(info, columns=['year','earnedrun', 'strikeout','homerun', 'hitted', 'pitchnum', 'dead4ball','losescore'],dtype='int64')
    scores = [(0,0,0,0,0,0)]
    for year in temp['year']:
        inning = innings[year][0]+round(innings[year][1]/3,2)
        ERA = float(round((9*temp[temp.year==year]['earnedrun'])/inning,3))
        FIP = float(round(((13*temp[temp.year==year]['homerun'] + 3*temp[temp.year==year]['dead4ball']-2*temp[temp.year==year]['strikeout'])/inning + 3.2),3))
        RA9 = float(round((temp[temp.year==year]['losescore']/inning)*9,3))
        OBP = float(round((temp[temp.year==year]['hitted']+temp[temp.year==year]['dead4ball'])/(temp[temp.year==year]['pitchnum']+temp[temp.year==year]['dead4ball']),3))
        AVG = float(round((temp[temp.year==year]['hitted']/temp[temp.year==year]['pitchnum']),3))
        scores.append((year, AVG, OBP, RA9, ERA, FIP))
    df= pd.DataFrame(scores[1:], columns=['YEAR','AVG','OBP','RA9','ERA','FIP'])
    df.replace(float('inf'), 0, inplace=True)
    df= df.fillna(0)
    return scores, df

def c_pitcher_inning_calculator(player_name):
    """특정 투수의 년도 별 이닝 수를 도출하는 함수
    """
    sql = f"SELECT scoreboard.year,pitcher.inning FROM pitcher INNER JOIN scoreboard ON pitcher.idx = scoreboard.idx WHERE pitcher.name = '{player_name}'"
    data = query_direct(sql)
    output = {}
    # 년도별 이닝과 나머지 계산
    for year, inning in data:
        if year not in output.keys():
            output[year] = [0,0]
        if len(str(inning)) == 1:
            output[year][1] += int(str(inning)[-1:])
        else:
            output[year][0] += int(str(inning)[:-1])
            output[year][1] += int(str(inning)[-1:])
    return output

def month_win_prop(team_name):
    if team_name == "키움":
        sql = f"SELECT month,count(result) FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') GROUP BY month" 
        sql_win = f"SELECT month,count(result) FROM scoreboard WHERE team IN ('키움','넥센','우리','히어로즈') and result = 1 GROUP BY month" 
    else:
        sql = f"SELECT month,count(result) FROM scoreboard WHERE team = '{team_name}' GROUP BY month" 
        sql_win = f"SELECT month,count(result) FROM scoreboard WHERE team = '{team_name}' and result = 1 GROUP BY month" 
    monthly = query_direct(sql)
    win_monthly = query_direct(sql_win)
    prop = []
    for i in range(len(monthly)):
        prop.append(win_monthly[i][1]/monthly[i][1])
    return prop
