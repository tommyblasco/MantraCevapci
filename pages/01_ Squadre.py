import streamlit as st
from datetime import date
from PIL import Image
import requests
from io import BytesIO
from funzioni import *

st.title("Squadre")

@st.cache
def load_images(team):
    url_stemma="https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/stemmi/"+team+".png".replace(' ','%20')
    url_maglie="https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/maglie/"+team+".png".replace(' ', '%20')
    url_pres = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/persone/"+team+" - pres.jpg".replace(' ', '%20')
    url_ds = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/persone/"+team+" - ds.jpg".replace(' ', '%20')
    url_mister = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/persone/"+team+" - mister.jpg".replace(' ', '%20')
    return [url_stemma, url_maglie, url_pres, url_ds, url_mister]

list_team=tuple(set([x for x in mercato['A'] if str(x) != 'nan']))

sel_team=st.selectbox('Scegli una squadra',list_team)

rosa=rosa_oggi(team=sel_team).drop('url',axis=1)
rosa['Data nascita']=[x.date() for x in rosa['Data nascita']]
rosa['Fine prest']=[x.date() for x in rosa['Fine prest']]
rosa['Indennizzo']=["€{:,.2f}".format(x) for x in rosa['Indennizzo']]

col1, col2 = st.columns(2)
with col1:
    st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[0]).content)))
with col2:
    st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[1]).content)))

tab1, tab2, tab3 = st.tabs(["Rosa attuale","Storia","Insights"])
with tab1:
    with st.expander("Organigramma"):
        col3, col4, col5 = st.columns(3)
        with col3:
            st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[2]).content)),caption='Presidente')
        with col4:
            st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[3]).content)),caption='DS')
        with col5:
            st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[4]).content)),caption='Mister')

    st.dataframe(rosa)

    with st.expander("Giocatori in prestito"):
        if prestito_players(team=sel_team).shape[0]>0:
            dflp=prestito_players(team=sel_team)
            dflp['TP']=[x.date() for x in dflp['TP']]
            st.dataframe(dflp)
        else:
            st.write("Nessun giocatore attualmente in prestito")
    with st.expander("Primavera"):
        if primav_players(team=sel_team).shape[0] > 0:
            dfpp = primav_players(team=sel_team)
            dfpp['TP'] = [x.date() for x in dfpp['TP']]
            st.dataframe(dfpp)
        else:
            st.write("Nessun giocatore attualmente in primavera")
with tab2:
    with st.expander("Palmares"):
        st.write("...")
    with st.expander("Cronistoria"):
        st.write("...")
with tab3:
    st.write("...") #grafici