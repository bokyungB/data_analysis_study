import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import plast_only_cols as col_info

pre_df = pd.read_excel('../data/plast_only.xlsx', header=[0, 1, 2, 3])
pre_df.columns = col_info.columns
x_axis_name, y_axis_name = '원료_Catalyst_금속촉매_TIPT (PIA 대비)','실험결과_분석결과_Coversion_Coversion'
x_col, y_col = x_axis_name,y_axis_name

y_actual = pre_df[y_col]
pre_df.dropna(subset=[x_col,y_col],inplace=True)

df = pre_df.iloc[:,1:-1]

model = LinearRegression()
# 한개의 독립변수가 아닌, 여러개의 독립변수 적용 
model.fit(df,y_actual)
y_predict = model.predict(df)

# 결과 확인해보기
try:
    test_df = df
    test_df['y_actaul'] = y_actual
    test_df['y_predict'] = y_predict
    test_df.to_csv('model_result_check.csv')
except:
    pass

fig =  go.Figure([go.Scatter(x=y_predict, y=y_actual, mode = 'markers')])
fig.show()