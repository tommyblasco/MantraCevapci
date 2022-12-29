import streamlit as st
from datetime import date
from PIL import Image
from funzioni import *

st.set_page_config(page_title="Mantra Cevapci")

st.title("Squadre")

list_team=tuple(set([x for x in mercato['A'] if str(x) != 'nan']))

sel_team=st.selectbox('Scegli una squadra',list_team)

rosa=rosa_oggi(team=sel_team).drop('url',axis=1)
rosa['Data nascita']=[x.date() for x in rosa['Data nascita']]
rosa['Fine prest']=[x.date() for x in rosa['Fine prest']]
rosa['Indennizzo']=["€{:,.2f}".format(x) for x in rosa['Indennizzo']]

col1, col2 = st.columns(2)
with col1:
    st.image(Image.open("https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/stemmi/"+sel_team+".png"))
with col2:
    st.image(Image.open("https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/maglie/"+sel_team+".png"))

tab1, tab2, tab3 = st.tabs(["Rosa attuale","Storia","Insights"])
with tab1:
    with st.expander("Organigramma"):
        st.write("...")
    st.dataframe(rosa)
    with st.expander("Giocatori in prestito"):
        st.write("...")
    with st.expander("Primavera"):
        st.write("...")
with tab2:
    with st.expander("Palmares"):
        st.write("...")
    with st.expander("Cronistoria"):
        st.write("...")
with tab3:
    st.write("...") #grafici