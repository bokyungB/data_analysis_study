import pandas as pd
import os , re
import numpy as np

df1 = pd.read_csv('test_re_02.csv',header=[0])
df2 = pd.read_csv('test_re_03.csv',header=[0])


print(df1.columns,df2.columns)

def df_cleaner(df,drop_col):
  drop_idx =[]
  for row in range(len(df)):
    if df1.isna().iloc[row,drop_col] == True:
      drop_idx.append(row)
    else:
      pass
  df_clean = df1.drop(drop_idx).reset_index(drop=True)
  return df_clean

df1_clean = df_cleaner(df1,6)
df2_clean = df_cleaner(df2,6)

df_process = pd.concat([df1_clean,df2_clean]).reset_index(drop=True)
df_drop_col = df_process.dropna(axis='columns',how='all')

## na 집계 : df.isna().sum()
## 특정열 drop : df.drop('column_name',axis=1)

print(df_drop_col.isna().sum())
# df_target = df_drop_col.drop(col_name,axis=1)
df_drop_col.to_csv('re_df_clean.csv',index=False , encoding='utf-8-sig',sep=',')