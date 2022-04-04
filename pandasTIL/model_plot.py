import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import plast_only_cols as col_info

df = pd.read_excel('../data/plast_only.xlsx', header=[0, 1, 2, 3])
df.columns = col_info.columns
x_axis_name, y_axis_name = '원료_Catalyst_금속촉매_TIPT (PIA 대비)','실험결과_분석결과_Coversion_Coversion'
x_col, y_col = x_axis_name,y_axis_name
df.dropna(subset=[x_col,y_col],inplace=True)
X = df[x_col]
Y = df[y_col]

model = LinearRegression()
model.fit(X.values.reshape(-1,1),Y)

y_range = model.predict(X.values.reshape(-1, 1))

fig = go.Figure([
    go.Scatter(x=X, y=Y, name='Actual', mode='markers'),
    go.Scatter(x=X, y=y_range, name='Prediction', mode='markers')
])
fig.show()