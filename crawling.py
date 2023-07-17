import datetime
from typing import Dict, List

import pymysql
import requests
from bs4 import BeautifulSoup as bs


def IPL_crawling() -> List[Dict] :
    """
    IPL 2023 경기 스케줄 크롤링
    """

    # IPL 2023 스케줄 url
    url = 'https://timesofindia.indiatimes.com/sports/cricket/ipl/schedule'

    response = requests.get(url)
    html_text = response.text
    soup = bs(html_text, 'html.parser')

    data = []

    # 파싱해서 dict로 데이터를 담는다
    for id, game in enumerate(soup.select('div.matchdetails')) :
        game_info = {}
        details = game.select('div')

        game_info['id'] = id+1
        game_info['title'] = details[2].text
        game_info['start_date'] = datetime.datetime.strptime(details[0].text, "%a, %d %B %Y")
        game_info['venue'] = details[1].text
        game_info['teams'] = details[3].text

        data.append(game_info)
    
    return data



def data_to_db(data:List[Dict], conn) -> None :
    """
    conn으로 연결된 db에 데이터를 업데이트
    """
    try:
        with conn.cursor() as curs: # 커서 할당
            # 테이블 생성
            query = '''
                    CREATE TABLE if not exists IPL2023 (
                        id int(11) NOT NULL PRIMARY KEY,
                        title varchar(255) NOT NULL,
                        start_date datetime NOT NULL,
                        venue varchar(255) NOT NULL,
                        teams varchar(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                        updated_at TIMESTAMP DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP NOT NULL
                    );
                    '''
            curs.execute(query)

            # 데이터 upsert
            if len(data) :
                query = (
                    f"INSERT INTO IPL2023 ({', '.join(data[0].keys())}) "
                    f"VALUES (%({')s, %('.join(data[0].keys())})s) "
                    f"ON DUPLICATE KEY UPDATE "
                    +
                    ', '.join([f'{k}=VALUES({k})' for k in data[0].keys()])
                )
            else :
                query = ''
            curs.executemany(query, data)
            inserted = curs.rowcount
    except:
        conn.rollback()
        print('IPL2023 table insert failed. Transaction rolled back')
        raise

    conn.commit()
    print('Upserted', inserted, 'row(s) into IPL2023 table')



def main() :
    data = IPL_crawling()
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} crawling finish')

    # db 연결
    conn = pymysql.connect(host='ipl_mysql', user='root', port=3306, password='1234', charset='utf8mb4', db='IPL_schedule')
    data_to_db(data, conn)
    conn.close()



if __name__ == "__main__" :
    main()