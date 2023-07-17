import unittest

import crawling
import pymysql


class IPLCrawlingTest(unittest.TestCase) :
    def test_IPL_crawling(self):
        # return 자료형 확인
        self.assertTrue(str(type(crawling.IPL_crawling())) == "<class 'list'>")
        self.assertTrue(str(type(crawling.IPL_crawling()[0])) == "<class 'dict'>")

        # 데이터가 한개 이상 크롤링 됐는지 확인
        self.assertTrue(len(crawling.IPL_crawling()) >= 1)

        # dict key 확인
        self.assertTrue(set(crawling.IPL_crawling()[0].keys()) == {'id','title','start_date','venue','teams'})
    
    def test_data_to_db(self):
        # data에 빈 배열이 들어간 경우 예외처리가 되었는지
        conn = pymysql.connect(host='localhost', user='root', port=3306, password='1234', charset='utf8mb4', db='IPL_schedule')
        self.assertTrue(crawling.data_to_db([],conn) == None)
        conn.close()

if __name__ == '__main__' :
    unittest.main()