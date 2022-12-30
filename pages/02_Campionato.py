import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from PIL import Image
import requests
from io import BytesIO
import plotly.graph_objects as go
from raceplotly.plots import barplot
from funzioni import *

st.title("Stats Campionato")

tab6, tab7, tab8, tab9 = st.tabs(["Classifiche stagionali","Classifica perpetua","Money","Top11"])
with tab6:
    sel_sea=st.selectbox('Scegli una stagione:',tuple(set(campionato['Stagione'])))
    cla=ranking(seas=sel_sea)
    contro_cla=controclass(seas=sel_sea)
    cla_arr=pd.merge(cla, contro_cla[['Team','Exp_Pnt']],left_on='Squadra',right_on='Team',how='left')
    cla_arr=cla_arr.drop('Team',axis=1)
    cla_arr['Delta']=[x-y for x,y in zip(cla_arr['Pnt'],cla_arr['Exp_Pnt'])]
    st.dataframe(cla_arr)
    with st.expander("Race Bar Chart"):
        df_cum=class_for_rbc(seas=sel_sea)
        bcr=barplot(df=df_cum,item_column='Squadra',value_column='CumP',time_column='Giornata')
        rbc=bcr.plot(time_label='Giornata',value_label='Punti',title='Evoluzione classifica',frame_duration=1000)
        st.plotly_chart(rbc, use_container_width=True)
with tab7:
    st.write('Classifica perpetua dagli albori')
    st.dataframe(ranking(seas='All'))
with tab8:
    st.write('...')
with tab9:
    st.write('...')
