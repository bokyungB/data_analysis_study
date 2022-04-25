import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm   
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score                 
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier    
from sklearn.neural_network import MLPRegressor,MLPClassifier            
from sklearn.model_selection import train_test_split
import pandas as pd
import data_plast_only_cols as col_info

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
def generate_model_graphs( id,x_prop, y_prop,model_name,data_now,selectedpoints):
    if (None not in (x_prop, y_prop)):
        try:
            ## selectedpoints 연결위해 1)index 복사-reset_index() 2) dropna 3) reset_index(drop=True)
            ## 이렇게 만들어진 pre_df 의 'index'라는 컬럼을 선택해 pre_df_idx를 만들어준다. 
            pre_df_withidx = data_now.reset_index()
            pre_df = pre_df_withidx.dropna(subset=[y_prop]).reset_index(drop=True)
            pre_df = pre_df.dropna(subset=x_prop).reset_index(drop=True)
            pre_df_idx = pre_df.loc[:,[id]]
            target_point = None
            y_actual = pre_df[y_prop]
            # df = adf = pre_df.iloc[:,2:-1]
            # print('check x_props',x_prop)
            df = pre_df.loc[:,x_prop]
            X = sm.add_constant(df)


            if model_name == 'MLR':
                model = sm.OLS(y_actual,X)
                result = model.fit()
            elif model_name == 'DT':
                model = DecisionTreeRegressor()
                result = model.fit(X,y_actual)

            elif model_name == 'ANN':
                node_num = len(X.columns)
                model = MLPRegressor(hidden_layer_sizes=( node_num ,))
                result = model.fit(X,y_actual)
            
            y_predict = result.predict(X)

            if model_name == 'MLR':
                rsquared = result.rsquared
                target_tbl = result.summary2().tables[1].loc[:,['Coef.','P>|t|']].round(3)
                target_tbl = target_tbl.reset_index().iloc[1:,:]
                model_result_col =[{'name': i, 'id': i} for i in target_tbl.columns]
                model_result_val = target_tbl.to_dict('records')
            else:
                rsquared = r2_score(y_actual, y_predict)
                print('DT or NR : ',rsquared)
                print(y_actual)
                print(y_predict)
                model_result_val = model_result_col = []
                
            model_result_rsquared = f'R² : {round(rsquared,3)}'    
                

            fig =  go.Figure(go.Scatter(x=y_predict, y=y_actual, text =pre_df[id],  mode = 'markers'))
            if selectedpoints:
                before_dropna_idx = np.intersect1d(pre_df_idx,[p['customdata'] for p in selectedpoints['points']]) 
                try:
                    print('pre_df_withidx index 확인', pre_df_withidx.index.tolist())
                    target_point = pre_df[pre_df['index'].isin(before_dropna_idx)].index.tolist()  
                    print('real target point ',target_point)
                except Exception as e:
                    print(e)
                    pass
            print('target_point:' ,target_point)
            fig.update_traces(
                                selectedpoints=target_point,
                                customdata = pre_df_idx,
            				    marker={ 'color': 'rgba(67, 67, 255, 0.7)', 'size': 10 },
                                selected={'marker': {'color': 'rgba(255, 67, 91, 0.7)' }},
            					unselected={'marker': { 'opacity': 0.3 , 'color': 'rgba(67, 67, 255, 0.7)' }})
            # print('config graph in generate_model_graphs function ', fig)
            
            fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5},dragmode='select',clickmode='event+select',hovermode = 'closest')
            # fig.update_xaxes(autorange=False)
        except Exception as e:
            print(e)  

x_values , y1,model_name ,raw_df,target_point = col_info.x_name, col_info.y_name, col_info.df , col_info.target_point
#  generate_model_graphs의 변수는 인터페이스에서 사용자 입력값으로 받아온다. 
model_fig1,mtable_val,mtable_col,rsquare = generate_model_graphs( id, x_values , y1,model_name ,raw_df,target_point)