import pandas as pd
import numpy as np
import sys

from db_connecting import db_connecting,db_connecting_kr
''' php -> python '''

part_comp_sql = "SELECT exp_profile_no,profile_value,exp_no FROM exp_profile WHERE profile_no = 2204101110120 AND history ='N'"

db_conn = db_connecting()

df = db_conn.query_excecute(part_comp_sql)

'''
    2021.03.31.금요일 개발서버 적용 전 샘플코드
    실험번호 'TEST_2009_01'과 같은 문자열을 나눠서 2009,01로 정렬을 해야함
    string value :  split df.칼럼명.str.rsplit(구분자)
    string to int , 에러 무시 : astype(int,errors = 'ignore')
    sort several columns 내림차순 : df.sorting_values([열1,열2],ascending=False)
    열 drop : df.drop(labels = [열1,열2] , axis=1 )
'''
df['sort_main'] = df.profile_value.str.rsplit("_").str[-2].astype(int,errors='ignore')
df['sort_sub'] = df.profile_value.str.rsplit("_").str[-1].astype(int,errors='ignore')
new_df = df.sort_values(['sort_main','sort_sub'],ascending=False).drop(labels=['sort_main','sort_sub'], axis=1)



