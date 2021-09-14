import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import streamlit as st
from plotly.validators import heatmap


def bar_chart(df_filtered):
    #---------
    dff_filtered = pd.DataFrame(df_filtered['var_obj_cat'].value_counts())
    dff_filtered.reset_index(inplace=True)
    dff_filtered.rename(columns={'index': 'Sentiment', 'var_obj_cat': '# of tweets'}, inplace=True)
    bar_chart = px.bar(dff_filtered, x="# of tweets", y="Sentiment", orientation='h', width=450, height=100)
    bar_chart.update_yaxes(title_font = {"size": 20}, title_standoff = 25)
    bar_chart.update_xaxes(title_text = "Number of Tweets", title_font = {"size": 18}, title_standoff = 25)
    bar_chart.update_traces(marker_color="#1898dc", marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
    bar_chart.update_layout(margin={"r":10,"t":10,"l":10,"b":10}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=390, font_color="#d58e1e")
    return bar_chart


def tweet_count(df_filtered):
    tweet_count = go.Figure(go.Indicator(mode = "number", 
                                        value = df_filtered.shape[0], 
                                        title = {'text':"# of Tweets", 'font_size': 18},
                                        number = {'prefix': "", 'valueformat':"  ", 'font_size': 34}, 
                                        domain = {'x': [0, 1], 'y': [0, 1]}))
    tweet_count.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', font_color="#d58e1e", margin={"r":0,"t":60,"l":0,"b":0}, height=160)
    return tweet_count


def pie_chart(df_filtered):
    df_pie = pd.DataFrame(df_filtered['retweeted'].value_counts())
    df_pie.reset_index(inplace=True)

    pie_chart=px.pie(
        data_frame=df_pie,
        names='index',
        values='retweeted',
        color_discrete_sequence=['#233cca', '#1898dc'],
        hole=.5,
        labels={'retweeted':'retweeted'},
        width=400, 
        height=200
    )
    pie_chart.update_layout(margin={"r":10,"t":10,"l":10,"b":10}, paper_bgcolor='rgba(0,0,0,0)', font_color="#d58e1e", font_size=10, height=300)
    pie_chart.update_layout(title={'text': "Is Retweet?", 'y':0.59, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    pie_chart.update_layout(legend=dict(x=0.4, y=.45, traceorder="normal", font=dict(family="sans-serif",size=12)))
    return pie_chart


def line_chart(df_filtered):
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
            },
        width=500, 
        height=250
    )
    line_chart.update_xaxes(title_font = {"size": 20}, title_standoff = 25)
    line_chart.update_yaxes(title_text = "Number of Tweets", title_font = {"size": 20}, title_standoff = 25)
    line_chart.update_layout(uirevision='foo')
    line_chart.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                     height=390, font_color="#d58e1e")
    line_chart.update_layout(legend=dict(x=.15, y=.95, traceorder="normal", font=dict(family="sans-serif",size=12)))
    return line_chart


def heat_map(df_filtered):
    #----------

    data = pd.DataFrame(df_filtered.groupby(['created_at_hour', 'var_obj_cat'])['text'].count())
    data.reset_index(inplace=True)
    data.rename(columns={'text': '# of Tweets'}, inplace=True)
    data = data.pivot(index='var_obj_cat', columns='created_at_hour', values='# of Tweets')
    
    values = data.values
    x = list(data.axes[1])
    y = list(data.axes[0])

    heat_map = ff.create_annotated_heatmap(values, x=x, y=y, annotation_text=values, colorscale=['#1898dc', '#233cca'])
    heat_map.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor='rgba(0,0,0,0)', height=350, font_color="#d58e1e")
    return heat_map


def tree_map(df_filtered):
    data = pd.DataFrame(df_filtered.groupby(['topic', 'var_obj_cont', 'var_obj_cat'])['text'].count())
    data1 = pd.DataFrame(df_filtered.groupby(['topic'])['var_obj_cont'].mean())
    data2 = pd.DataFrame(df_filtered.groupby(['topic'])['text'].count())
    data = data1.merge(data2, left_index=True, right_index=True)
    data.reset_index(inplace=True)
    data.rename(columns={'text': '# of Tweets'}, inplace=True)
    tree_map = px.treemap(data, path=['topic'], values='# of Tweets',
                color='var_obj_cont',
                #color_continuous_scale=["#f43034", "#f2e87b", "#33CE55"],
                color_continuous_scale=["red","yellow", "green"],
                color_continuous_midpoint=np.average(data['var_obj_cont'], weights=data['# of Tweets']))
    tree_map.update_coloraxes(showscale=False)
    tree_map.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor='rgba(0,0,0,0)', height=350, font_color="#d58e1e")
    return tree_map


def dense_map(df_filtered):
    data = pd.DataFrame(df_filtered.groupby(['user_location'])['var_obj_cont'].mean())
    data.reset_index(inplace=True)
    dense_map = go.Figure(data=go.Choropleth(locations=data['user_location'], 
                                            z = data['var_obj_cont'].astype(float),
                                            locationmode = "country names",
                                            colorscale =["#f43034", "#f2e87b", "#33CE55"],
                                            colorbar_title = "Sentiment Level",))
    dense_map.update_layout(geo_scope='world')
    dense_map.update_layout(margin={"r":20,"t":20,"l":20,"b":20}, paper_bgcolor='rgba(0,0,0,0)', height=390, font_color="#d58e1e")
    return dense_map


def half_donut(df_filtered):
    half_donut = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]},
                                        value = df_filtered['var_obj_cont'].mean(),
                                        mode = "gauge+number+delta",
                                        title = {'text': "Average Sentiment", 'font_size': 14},
                                        gauge = {'axis': {'range': [None, 1]},
                                                'bar': {'color': '#233cca'},
                                                'steps' : [
                                                    {'range': [0, 0.4], 'color': "#B97263"},
                                                    {'range': [0.41, 0.6], 'color': "#F3C67B"},
                                                    {'range': [0.61, 1], 'color': "#C1DCBE"}]}))
    half_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin={"r":10,"t":55,"l":10,"b":0}, height=160, font = {'color': "#d58e1e"})
    return (half_donut)