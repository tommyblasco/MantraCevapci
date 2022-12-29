import streamlit as st
from datetime import date
from PIL import Image
import requests
from io import BytesIO
import plotly.graph_objects as go
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
@st.cache
def load_images_cup():
    url_camp = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/cups/Campionato.png"
    url_luk = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/cups/Coppa%20Luk.png"
    url_iva = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/cups/Supercoppa%20Ivanica.png"
    url_ulmi = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/cups/Ulmi.png"
    return [url_camp, url_luk, url_iva, url_ulmi]

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
    st.header("Rosa attuale")
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
    col6, col7, col8, col9 = st.columns(4)
    with col6:
        his_camp=cronistoria(team=sel_team,comp="MantraCevapci")
        st.image(Image.open(BytesIO(requests.get(load_images_cup()[0]).content)), caption='Titoli: '+str(his_camp[his_camp['Risultato']=='Vincitore'].shape[0]))
        st.dataframe(his_camp)
    with col7:
        his_luk = cronistoria(team=sel_team, comp="Coppa Luk")
        st.image(Image.open(BytesIO(requests.get(load_images_cup()[1]).content)), caption='Titoli: '+str(his_luk[his_luk['Risultato']=='Vincitore'].shape[0]))
        st.dataframe(his_luk)
    with col8:
        his_iva = cronistoria(team=sel_team, comp="Supercoppa Ivanica")
        st.image(Image.open(BytesIO(requests.get(load_images_cup()[2]).content)), caption='Titoli: '+str(his_iva[his_iva['Risultato']=='Vincitore'].shape[0]))
        if his_iva.shape[0]>0:
            st.dataframe(his_iva)
    with col9:
        his_ulmi = cronistoria(team=sel_team, comp="ULMI")
        st.image(Image.open(BytesIO(requests.get(load_images_cup()[3]).content)), caption='Titoli: '+str(his_ulmi[his_ulmi['Risultato']=='Vincitore'].shape[0]))
        if his_ulmi.shape[0] > 0:
            st.dataframe(his_ulmi)
with tab3:
    n_rosa = go.Figure(go.Indicator( domain={'x': [0, 1], 'y': [0, 1]},
        value=rosa.shape[0], mode="gauge+number", title={'text': "Giocatori in rosa"},
        gauge={'axis': {'range': [None, 40]}, 'steps': [
                   {'range': [0, rosa.shape[0]-primav_players(team=sel_team).shape[0]], 'color': "lightgray"},
                   {'range': [rosa.shape[0]-primav_players(team=sel_team).shape[0], rosa.shape[0]], 'color': "gray"}]}))
    st.plotly_chart(n_rosa)