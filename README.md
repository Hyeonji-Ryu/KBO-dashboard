

## 한국야구위원회 데이터 분석 대시보드 (KBO analytical dashboard)

![git](https://user-images.githubusercontent.com/42489770/117327030-2b205500-aecd-11eb-937f-438108cbbee3.jpg)

위 대시보드는 현재 진행중인 KBO 프로젝트에서 크롤링하여 얻은 데이터를 시각화하기 위해 만들었습니다.  
I made this dashboard to visualize the data obtained by crawling from KBO project.  

공개한 소스 코드에 포함된 sqlite 파일은 테스트를 위한 임시 데이터베이스이기에 시각화된 그래프 또한 통계적 의미는 없습니다.    
The sqlite file in the source code is a temporary database for testing, So visualized graphs are meaningless.

실제 데이터를 반영한 대시보드는 몇 가지 수정을 거친 후 AWS에 배포할 예정입니다.   
The dashboard updating the actual data will be published on AWS after some modifications.  

### 웹 프레임워크 (Web Framework)
- Flask
- Dash

### CSS 프레임워크 (CSS Framework)
- Bootstrap5 alpha2

### 시각화 라이브러리 (Visualization Tools)
- Plotly

### 서버 (Server)
- will be changed from AWS ec2 to AWS lightsail

### 데이터베이스 (Database)
- mariaDB
