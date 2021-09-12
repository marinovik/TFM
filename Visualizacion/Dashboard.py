import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import os

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.validators import heatmap

app = dash.Dash(__name__)
server = app.server

#---------------------------------------------------------------
df = pd.read_csv("df_completo.csv")
dff = df[['text', 'retweeted', 'user_location', 'created_at_hour', 'topic', 'var_obj_cont', 'var_obj_cat']]
dff.sort_values(by='created_at_hour', inplace=True)
dff[:5]

#---------------------------------------------------------------


app.layout = html.Div([

    html.Div([
        html.H1('Twitter Sentiment Analysis Dashboard', style={'textAlign': 'center', 'color': 'rgb(194,194,191)'})
    ]),
    
    
    html.Div([

        html.Div([
            
            dcc.Dropdown(id='Sentimentdropdown',
                options=[
                         {'label': 'Positive', 'value': 'positive'},
                         {'label': 'Neutral', 'value': 'neutral'},
                         {'label': 'Negative', 'value': 'negative'}],
                value='var_obj_cat',
                multi=True,
                placeholder='Sentiment',
                clearable=False,
                style={'display': "inline-block", 'width': '100%', 'margin-bottom':4}
            ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='RTdropdown',
            options=[
                     {'label': 'True', 'value': 'Si'},
                     {'label': 'False', 'value': 'No'}
            ],
            value='retweet',
            placeholder='Retweet',
            multi=True,
            clearable=False,
            style={'display': "inline-block", 'width': '100%', 'margin-bottom':4}
        ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='Locationdropdown',
            options=[
                     {'label': 'United States', 'value': 'United States'},
                     {'label': 'Spain', 'value': 'Spain'},
                     {'label': 'Italy', 'value': 'Italy'},
                     {'label': 'Germany', 'value': 'Germany'},
                     {'label': 'France', 'value': 'France'}
            ],
            value='location',
            placeholder='Location',
            multi=True,
            clearable=False,
            style={'display': "inline-block", 'width': '100%', 'margin-bottom':4}
        ),
        ],className='six columns'),

        html.Div([
            dcc.Dropdown(id='Topicdropdown',
                options=[
                         {'label': 'Business', 'value': 'Business'},
                         {'label': 'Automotive', 'value': 'Automotive'},
                         {'label': 'Social', 'value': 'Social'},
                         {'label': 'Science', 'value': 'Science'},
                         {'label': 'Sports', 'value': 'Sports'},
                         {'label': 'Food', 'value': 'Food'}
                ],
                value='var_obj_cat',
                multi=True,
                placeholder='Topic',
                clearable=False,
            style={'display': "inline-block", 'width': '100%', 'margin-bottom':4}
            ),
        ],className='six columns'),

    ],style={'display': 'flex', 'margin-bottom': 50, 'margin-left': 50, 'margin-right': 50}, className='row'), 

    


    html.Div([

        html.Div([
            html.Div([dcc.Graph(id='tweetcount', style={'margin':2, 'height': 'auto'}),
            ],style={'height': '200px','border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e'},className='row'),

            html.Div([dcc.Graph(id='halfdonut', style={'margin':2, 'height': 'auto'}) 
            ],style={'height': '200px','border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e'},className='row')
        ], style={'width': '15%','height': '400px','border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e', 'margin-left': 10, 'margin-right': 10}, className='six columns'),

        html.Div([
            dcc.Graph(id='linechart', style={'margin':5, 'height': 'auto'}),
        ],style={'width': '45%', 'height': '400px', 'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e', 'margin-left': 10, 'margin-right': 10}, className='six columns'),

        html.Div([
            dcc.Graph(id='barchart', style={'margin':5}),
        ],style={'width': '25%', 'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e', 'margin-left': 10, 'margin-right': 10},className='six columns'),

        html.Div([
            dcc.Graph(id='piechart', style={'margin':5, 'height': 'auto'}),
        ],style={'width': '15%', 'height': '400px', 'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e', 'margin-left': 10, 'margin-right': 10},className='six columns'),


    ],style={'display': 'flex', 'margin-bottom': 20, 'margin-left': 20, 'margin-right': 20}, className='row'),

    html.Div([

        html.Div([
            dcc.Graph(id='treemap', style={'margin':5}),
        ],style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e', 'margin-left': 10, 'margin-right': 10},className='six columns'),

        html.Div([
            dcc.Graph(id='densemap', style={'margin':5}),
        ],style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e', 'margin-left': 10, 'margin-right': 0},className='six columns'),

    ],style={'height': '400px', 'display': 'flex', 'margin-bottom': 20, 'margin-left': 20, 'margin-right': 0}, className='row'),


    html.Div([
        html.Div([
            dcc.Graph(id='heatmap', style={'margin':5}),
        ],style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#1d264e'},className='six columns'),


    ],style={'height': '400px','display': 'flex', 'margin-bottom': 50, 'margin-left': 50, 'margin-right': 50}, className='row'),

    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 5,
            
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px',
                'textAlign': 'left',
            },
        ),
    ],style={'display': 'flex', 'margin-bottom': 50, 'margin-left': 50, 'margin-right': 50},className='row'),


],style={'backgroundColor':'#18203a'}) 

#------------------------------------------------------------------
@app.callback(
    [Output('tweetcount', 'figure'),
     Output('piechart', 'figure'),
     Output('linechart', 'figure'),
     Output('barchart', 'figure'),
     Output('heatmap', 'figure'),
     Output('treemap', 'figure'),
     Output('densemap', 'figure'),
     Output('halfdonut', 'figure'),
     ],
    [Input('datatable_id', 'selected_rows'),
     Input('RTdropdown', 'value'),
     Input('Sentimentdropdown', 'value'),
     Input('Locationdropdown', 'value'),
     Input('Topicdropdown', 'value')
     ]
)

def update_data(chosen_rows,piedropval,linedropval, locationdropval, topicdropval):
    if len(chosen_rows)==0:
        #df_filtered = dff[dff['countriesAndTerritories'].isin(['China','Iran','Spain','Italy'])]
        df_filtered = dff
    else:
        print(chosen_rows)
        df_filtered = dff[dff.index.isin(chosen_rows)]


    #---------
    dff_filtered = pd.DataFrame(df_filtered['var_obj_cat'].value_counts())
    dff_filtered.reset_index(inplace=True)
    dff_filtered.rename(columns={'index': 'Sentiment', 'var_obj_cat': '# of tweets'}, inplace=True)
    bar_chart = px.bar(dff_filtered, x="# of tweets", y="Sentiment", orientation='h')
    bar_chart.update_yaxes(title_font = {"size": 20}, title_standoff = 25)
    bar_chart.update_xaxes(title_text = "Number of Tweets", title_font = {"size": 18}, title_standoff = 25)
    bar_chart.update_traces(marker_color='#93C9FF', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
    bar_chart.update_layout(margin={"r":10,"t":10,"l":10,"b":10}, paper_bgcolor="#1d264e", plot_bgcolor='rgba(0,0,0,0)', height=390, font_color="#d58e1e")
    #---------

    tweet_count = go.Figure(go.Indicator(mode = "number", 
                                         value = df_filtered.shape[0], 
                                         title = {'text':"# of Tweets", 'font_size': 18},
                                         number = {'prefix': "", 'valueformat':"  ", 'font_size': 34}, 
                                         domain = {'x': [0, 1], 'y': [0, 1]}))
    tweet_count.update_layout(paper_bgcolor = "#1d264e", font_color="#d58e1e", margin={"r":0,"t":60,"l":0,"b":0}, height=160)
    #----------
    df_pie = pd.DataFrame(df_filtered['retweeted'].value_counts())
    df_pie.reset_index(inplace=True)

    pie_chart=px.pie(
        data_frame=df_pie,
        names='index',
        values='retweeted',
        color_discrete_sequence=['#9090C7', '#4646A2'],
        hole=.5,
        labels={'retweeted':'retweeted'}
    )
    pie_chart.update_layout(margin={"r":20,"t":0,"l":20,"b":20}, paper_bgcolor="#1d264e", font_color="#d58e1e", font_size=14, height=390)
    pie_chart.update_layout(title={ 'text': "Is Retweet?", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    pie_chart.update_layout(legend=dict(x=.5, y=.0, traceorder="normal", font=dict(family="sans-serif",size=12)))
    #----------

    data = pd.DataFrame(df_filtered.groupby(by=['created_at_hour', 'var_obj_cat']).count())
    data.reset_index(inplace=True)
    dff_filtered = data[['created_at_hour', 'var_obj_cat', 'text']]
    dff_filtered.rename(columns={'created_at_hour': 'Hour', 'var_obj_cat': 'Sentiment', 'text': '# of tweets'}, inplace=True)
    dff_filtered.sort_values(by='Hour', inplace=True)

    line_chart = px.line(
        data_frame=dff_filtered,
        x='Hour',
        y='# of tweets',
        color='Sentiment',
        color_discrete_map={
                 "Negativo": 'rgb(187,14,26)',
                 "Neutro": 'rgb(254,218,63)',
                 "Positivo": 'rgb(52,191,69)',
             }
    )
    line_chart.update_xaxes(title_font = {"size": 20}, title_standoff = 25)
    line_chart.update_yaxes(title_text = "Number of Tweets", title_font = {"size": 20}, title_standoff = 25)
    line_chart.update_layout(uirevision='foo')
    line_chart.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor="#1d264e", plot_bgcolor='rgba(0,0,0,0)', height=390, font_color="#d58e1e")
    line_chart.update_layout(legend=dict(x=.15, y=.95, traceorder="normal", font=dict(family="sans-serif",size=12)))
    #----------

    data = pd.DataFrame(df_filtered.groupby(['created_at_hour', 'var_obj_cat'])['text'].count())
    data.reset_index(inplace=True)
    data.rename(columns={'text': '# of Tweets'}, inplace=True)
    data = data.pivot(index='var_obj_cat', columns='created_at_hour', values='# of Tweets')
    
    values = data.values
    x = list(data.axes[1])
    y = list(data.axes[0])

    heat_map = ff.create_annotated_heatmap(values, x=x, y=y, annotation_text=values, colorscale='Viridis')
    heat_map.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor="#1d264e", height=390, font_color="#d58e1e")
    #-----------

    data = pd.DataFrame(df_filtered.groupby(['topic', 'var_obj_cont', 'var_obj_cat'])['text'].count())
    data1 = pd.DataFrame(df_filtered.groupby(['topic'])['var_obj_cont'].mean())
    data2 = pd.DataFrame(df_filtered.groupby(['topic'])['text'].count())
    data = data1.merge(data2, left_index=True, right_index=True)
    data.reset_index(inplace=True)
    data.rename(columns={'text': '# of Tweets'}, inplace=True)
    tree_map = px.treemap(data, path=['topic'], values='# of Tweets',
                  color='var_obj_cont',
                  #color_continuous_scale=["#f43034", "#f2e87b", "#33CE55"],
                  color_continuous_scale=["red","orange", "green"],
                  color_continuous_midpoint=np.average(data['var_obj_cont'], weights=data['# of Tweets']))
    tree_map.update_coloraxes(showscale=False)
    tree_map.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor="#1d264e", height=390, font_color="#d58e1e")
    #-----------

    data = pd.DataFrame(df_filtered.groupby(['user_location'])['var_obj_cont'].mean())
    data.reset_index(inplace=True)
    dense_map = go.Figure(data=go.Choropleth(locations=data['user_location'], 
                                             z = data['var_obj_cont'].astype(float),
                                             locationmode = "country names",
                                             colorscale =["#f43034", "#f2e87b", "#33CE55"],
                                             colorbar_title = "Sentiment Level",))
    dense_map.update_layout(geo_scope='world')
    dense_map.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor="#1d264e", height=390, font_color="#d58e1e")


    #-----------


    half_donut = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]},
                                        value = df['var_obj_cont'].mean(),
                                        mode = "gauge+number+delta",
                                        title = {'text': "Average Sentiment", 'font_size': 14},
                                        gauge = {'axis': {'range': [None, 1]},
                                                 'bar': {'color': "#C2BFBF"},
                                                 'steps' : [
                                                     {'range': [0, 0.4], 'color': "#B97263"},
                                                     {'range': [0.41, 0.6], 'color': "#F3C67B"},
                                                     {'range': [0.61, 1], 'color': "#C1DCBE"}]}))
    half_donut.update_layout(paper_bgcolor="#1d264e", margin={"r":10,"t":55,"l":10,"b":0}, height=160, font = {'color': "#d58e1e"})

    return (tweet_count, pie_chart,line_chart, bar_chart, heat_map, tree_map, dense_map, half_donut)


#------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
