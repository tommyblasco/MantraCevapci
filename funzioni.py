# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:31:20 2020

@author: user
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta, date
import streamlit.components.v1 as components
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import plotly.graph_objects as go
from raceplotly.plots import barplot

stagione_in_corso='2022-23'

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
    url_campo = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/cups/campo.png"
    url_cards = "https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/images/cups/Card.png"
    return [url_camp, url_luk, url_iva, url_ulmi,url_campo,url_cards]

@st.cache
def load_data(df):
    l_data=pd.read_csv("https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/Dati/"+df+".csv",sep=";",decimal=",")
    return l_data

ruolo=load_data("Ruolo")
campionato=load_data("Campionato")
giocatori=load_data("Giocatori")
deco_prizes=load_data("Deco_prizes")
premi_extra=load_data("Premi_extra")
mercato=load_data("Mercato")
quotazioni=load_data("Quotazioni_new")
voti=load_data("Voti_new")
moduli=load_data("Moduli")
grafica=load_data("Grafica")
albo_doro=load_data("Albo_doro")

voti['Data']=voti['Data'].apply(pd.to_datetime, format="%d/%m/%Y")
mercato['Data']=mercato['Data'].apply(pd.to_datetime, format="%d/%m/%Y")
mercato['TP']=mercato['TP'].apply(pd.to_datetime, format="%d/%m/%Y")
giocatori['Data_nascita']=giocatori['Data_nascita'].apply(pd.to_datetime, format="%d/%m/%Y")
mercato['deco_op']=['PRE' if x.startswith('PRE') else x for x in mercato['Tipo_operazione']]
ruoli_dif=['Por','DD; DS; E','DC','DD; DC','DS; DC','DD; DC; E','DS; DC; E','DD; DS; E','DS; E','DD; E','DD; E; M','DS; E; M','DD; DS; DC']
ruoli_cen=['E','E; M','E; W','E; C','M; C','M','C; T','C','C; W','C; W; T','W','W; T','T']
ruoli_att=['W; A','W; T; A','T; A','A','PC']

#voti con stipendi e fv
def voti_arricchiti():
    vo_ru=pd.merge(voti,ruolo,on=['Nome','Stagione'],how='left')
    vo_ru_me=pd.merge(vo_ru,mercato[['Nome','Data','TP','A']],on='Nome',how='left')
    voti_arr=vo_ru_me[(vo_ru_me['Data_x']>vo_ru_me['Data_y'])&(vo_ru_me['Data_x']<vo_ru_me['TP'])].drop('Data_y',axis=1).drop('TP',axis=1)
    voti_arr.rename(columns={'Data_x':'Data','A':'Squadra'},inplace=True)
    voti_arr['PInv']=[1 if (x==0) & (y=='Por') else 0 for x,y in zip(voti_arr['Gs'],voti_arr['Ruolo'])]
    voti_arr['Stipendio']=[a*0.15+b*0.15+c*0.1+d*0.05+e*0.05 for a,b,c,d,e in zip(voti_arr['Gf'],voti_arr['Rp'],voti_arr['Rf'],voti_arr['PInv'],voti_arr['Ass'])]
    voti_arr['FV']=[a+b*3-c+d*3-e*2+f*2-g*2-h*0.5-i+j for a,b,c,d,e,f,g,h,i,j in zip(voti_arr['Voto'],voti_arr['Gf'],voti_arr['Gs'],voti_arr['Rp'],voti_arr['Rs'],voti_arr['Rf'],voti_arr['Au'],voti_arr['Amm'],voti_arr['Esp'],voti_arr['Ass'])]
    voti_arr['FV']=[6 if np.isnan(x) else y for x,y in zip(voti_arr['Gf'],voti_arr['FV'])]
    voti_arr['Stipendio']=voti_arr['Stipendio'].fillna(0)
    return voti_arr

#classifica x tutte le stagioni
def ranking(seas):
    if seas=='All':
        db=campionato
    else:
        db=campionato[campionato['Stagione']==seas]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GH'],db['GA'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GH'],db['GA'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GH'],db['GA'])]
    db['PH']=[x*3+y for x,y in zip(db['H'],db['N'])]
    db['PA']=[x*3+y for x,y in zip(db['A'],db['N'])]
    casa=db.groupby(['Home'],as_index=False).agg({'PH':'sum','H':'sum','N':'sum','A':'sum','GH':'sum','GA':'sum','PntH':'sum'})
    trasferta=db.groupby(['Away'],as_index=False).agg({'PA':'sum','A':'sum','N':'sum','H':'sum','GA':'sum','GH':'sum','PntA':'sum'})
    casa.columns=['Squadra','Pnt','V','N','P','GF','GS','PntGlob']
    trasferta.columns=['Squadra','Pnt','V','N','P','GF','GS','PntGlob']
    classifica=casa.append(trasferta).groupby(['Squadra'],as_index=False).agg({'Pnt':'sum','V':'sum','N':'sum','P':'sum','GF':'sum','GS':'sum','PntGlob':'sum'})

    #penalizzazioni
    def apply_penalty(t,p):
        classifica.loc[classifica['Squadra']==t,'Pnt']=classifica.loc[classifica['Squadra']==t,'Pnt']-p
        return classifica
    if seas=='2020-21':
        apply_penalty('Agghiaggiande',5)
    elif seas=='2022-23':
        apply_penalty('Olympique Bidet',1)

    classifica=classifica.sort_values(by=['Pnt','PntGlob'],ascending=False)
    classifica.insert(0,'Pos',list(range(1,11)))
    return classifica

def class_for_rbc(seas):
    db=campionato[campionato['Stagione']==seas]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GH'],db['GA'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GH'],db['GA'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GH'],db['GA'])]
    db['PH']=[x*3+y for x,y in zip(db['H'],db['N'])]
    db['PA']=[x*3+y for x,y in zip(db['A'],db['N'])]
    casa=db[['Home','Giornata','PH']]
    casa.columns=['Squadra','Giornata','Pnt']
    tras = db[['Away', 'Giornata', 'PA']]
    tras.columns = ['Squadra', 'Giornata', 'Pnt']
    db_tot=casa.append(tras)
    if seas=='2020-21':
        db_tot.loc[(db_tot['Squadra']=='Agghiaggiande')&(db_tot['Giornata']==1),'Pnt']=db_tot.loc[(db_tot['Squadra']=='Agghiaggiande')&(db_tot['Giornata']==1),'Pnt']-5
    if seas=='2022-23':
        db_tot.loc[(db_tot['Squadra']=='Olympique Bidet')&(db_tot['Giornata']==1),'Pnt']=db_tot.loc[(db_tot['Squadra']=='Olympique Bidet')&(db_tot['Giornata']==1),'Pnt']-1
    db_tot = db_tot.sort_values(by=['Giornata'])
    db_tot['CumP'] = db_tot.groupby(['Squadra'], as_index=False)['Pnt'].transform(pd.Series.cumsum)
    return db_tot

#bilancio
def billato(seas):
    mk=mercato[mercato['Stagione']==seas]
    ms=sum(voti_arricchiti().loc[(voti_arricchiti()['Squadra']!='') & (voti_arricchiti()['Stagione']==seas),'Stipendio'])
    cl_pre=pd.merge(ranking(seas),premi_extra[premi_extra['Stagione']==seas],on=['Squadra'],how='left')
    cl_pre_d=pd.merge(cl_pre,deco_prizes[deco_prizes['Stagione']==seas],on=['Pos'],how='left')
    cl_pre_d['Stipendio']=[ms]*cl_pre_d.shape[0]
    cl_pre_d['Prize_Cup']=cl_pre_d['Prize_Cup'].fillna(0)
    cl_pre_d['Tot']=[a+b+c*d for a,b,c,d in zip(cl_pre_d['Prize_Cup'],cl_pre_d['Fisso'],cl_pre_d['Percentuale'],cl_pre_d['Stipendio'])]
    premi=cl_pre_d[['Squadra','Tot']]
    premi.insert(1,'Voce',['Premi']*premi.shape[0])
    ricavi=mk.groupby(['Da','deco_op'],as_index=False).agg({'Entrata_Da':'sum'})
    ricavi.rename(columns={'Da':'Squadra','deco_op':'Voce','Entrata_Da':'Tot'},inplace=True)

    entrate_fin=pd.concat([premi,ricavi])
    entrate_fin.insert(2,'Flusso',['Entrata']*entrate_fin.shape[0])

    v = voti_arricchiti()[voti_arricchiti()['Stagione']==seas]
    stip=v.groupby(['Squadra'],as_index=False).agg({'Stipendio':'sum'})
    stip.insert(1,'Voce',['Stipendi']*stip.shape[0])
    stip.rename(columns={'Stipendio':'Tot'},inplace=True)
    contracts=mk.groupby(['A'],as_index=False).agg({'Costo_contratto':'sum'})
    contracts.rename(columns={'Costo_contratto':'Tot','A':'Squadra'},inplace=True)
    contracts.insert(1,'Voce',['Contratti']*contracts.shape[0])
    tm_quot=mk['A'].drop_duplicates()
    vc_quot=['Quota']*len(tm_quot)
    tot_quot=[40]*len(tm_quot)
    quots=pd.DataFrame({'Squadra':tm_quot,'Voce':vc_quot,'Tot':tot_quot})
    costi=mk.groupby(['A','deco_op'],as_index=False).agg({'Spesa_A':'sum'})
    costi.rename(columns={'A':'Squadra','deco_op':'Voce','Spesa_A':'Tot'},inplace=True)

    spese_fin=pd.concat([stip,contracts,quots,costi])
    spese_fin['Tot']=[x*(-1) for x in spese_fin['Tot']]
    spese_fin.insert(2,'Flusso',['Spesa']*spese_fin.shape[0])

    bilancio_fin=pd.concat([spese_fin,entrate_fin])
    return bilancio_fin

# rose actual
def rosa_oggi(team):
    market_now = mercato[(mercato['Data'] <= datetime.today()) & (mercato['TP'] > datetime.today()) & (mercato['A']==team)]
    gio_con = pd.merge(giocatori, market_now[['Nome', 'Tipo_operazione', 'TP']], left_on='ID', right_on='Nome',how='inner')
    gio_con_r = pd.merge(gio_con, ruolo[ruolo['Stagione'] == max(ruolo['Stagione'])], left_on='ID', right_on='Nome',how='left')
    gio_con_rq = pd.merge(gio_con_r, quotazioni[quotazioni['Stagione'] == max(quotazioni['Stagione'])], left_on='ID',right_on='Nome', how='left')
    gio_con_rq = gio_con_rq.drop('Nome_y', axis=1).drop('Stagione_y', axis=1).drop('Stagione_x', axis=1)
    gio_con_rq.columns = ['ID', 'Nome', 'Data nascita', 'Luogo nascita', 'Nazionalità', 'url', 'Contratto', 'Fine prest',
                           'b', 'Ruolo', 'QI', 'QA', 'Diff', 'VI', 'VA', 'VFA']
    gio_con_rq = gio_con_rq.drop('b', axis=1)
    gio_con_rq['Età'] = [(datetime.today() - x) // timedelta(days=365.2425) for x in gio_con_rq['Data nascita']]

    def cond_indenn(x):
        if (((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) >= 1) & (x['Ruolo'] in ruoli_dif) & (
                x['QA'] * 0.1 >= x['VA'])) | (
                ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) >= 1) & (x['Ruolo'] in ruoli_cen) & (
                x['QA'] * 0.2 >= x['VA'])) | (
                ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) >= 1) & (x['Ruolo'] in ruoli_att) & (
                x['QA'] * 0.3 >= x['VA'])):
            return round(max(x['VA'], 0.05), 2)
        elif ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) >= 1) & (x['Ruolo'] in ruoli_dif) & (
                x['QA'] * 0.1 < x['VA']):
            return round(max(x['QA'] * 0.1, 0.05), 2)
        elif ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) >= 1) & (x['Ruolo'] in ruoli_cen) & (
                x['QA'] * 0.2 < x['VA']):
            return round(max(x['QA'] * 0.2, 0.05), 2)
        elif ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) >= 1) & (x['Ruolo'] in ruoli_att) & (
                x['QA'] * 0.3 < x['VA']):
            return round(max(x['QA'] * 0.3, 0.05), 2)
        elif (((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) < 1) & (x['Ruolo'] in ruoli_dif) & (
                x['QA'] * 0.1 >= x['VA'])) | (
                ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) < 1) & (x['Ruolo'] in ruoli_cen) & (
                x['QA'] * 0.2 >= x['VA'])) | (
                ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) < 1) & (x['Ruolo'] in ruoli_att) & (
                x['QA'] * 0.3 >= x['VA'])):
            return round(max(x['VA'] / 2, 0.05), 2)
        elif ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) < 1) & (x['Ruolo'] in ruoli_dif) & (
                x['QA'] * 0.1 < x['VA']):
            return round(max(x['QA'] * 0.1 / 2, 0.05), 2)
        elif ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) < 1) & (x['Ruolo'] in ruoli_cen) & (
                x['QA'] * 0.2 < x['VA']):
            return round(max(x['QA'] * 0.2 / 2, 0.05), 2)
        elif ((x['Fine prest'] - datetime.today()) // timedelta(days=365.2425) < 1) & (x['Ruolo'] in ruoli_att) & (
                x['QA'] * 0.3 < x['VA']):
            return round(max(x['QA'] * 0.3 / 2, 0.05), 2)

    gio_con_rq['Indennizzo'] = gio_con_rq.apply(cond_indenn, axis=1)
    return gio_con_rq[['Nome','Data nascita','Luogo nascita','Nazionalità','Età','Ruolo','Contratto','Fine prest','Indennizzo','url']]

def prestito_players(team):
    market_now = mercato[(mercato['Data'] <= datetime.today()) & (mercato['TP'] > datetime.today()) & (mercato['Da'] == team) & (mercato['deco_op']=='PRE')]
    gio_con = pd.merge(giocatori[['ID']], market_now[['Nome', 'A', 'Tipo_operazione', 'TP']], left_on='ID', right_on='Nome',how='inner').drop('ID',axis=1)
    gio_con_r = pd.merge(gio_con, ruolo[ruolo['Stagione'] == max(ruolo['Stagione'])], on='Nome',how='left')
    return gio_con_r

def primav_players(team):
    market_now = mercato[(mercato['Data'] <= datetime.today()) & (mercato['TP'] > datetime.today()) & (mercato['A'] == team) & (mercato['Primavera']=='P')]
    gio_con = pd.merge(giocatori[['ID']], market_now[['Nome', 'TP']], left_on='ID', right_on='Nome',how='inner').drop('ID',axis=1)
    gio_con_r = pd.merge(gio_con, ruolo[ruolo['Stagione'] == max(ruolo['Stagione'])], on='Nome',how='left')
    return gio_con_r

#b11
def b11(seas,gio):
    v_rist = voti_arricchiti()[(voti_arricchiti()['Stagione'] == seas) & (voti_arricchiti()['Giornata'] == gio) & (pd.notnull(voti_arricchiti()['Squadra']))]
    v = v_rist[['Nome', 'Ruolo', 'FV', 'Giornata', 'Squadra']]
    m = moduli[moduli['Stagione'] == seas]
    lg_sort = v.sort_values('FV', ascending=False)
    lg_sort = lg_sort[pd.notnull(lg_sort['FV'])]
    lg_sort.reset_index(drop=True, inplace=True)
    f_df=pd.DataFrame()
    for modul in list(set(m['Modulo'])):
        modulis=m[m['Modulo']==modul]
        df=pd.merge(lg_sort,modulis,on='Ruolo',how='left')
        df['Pos']=df.iloc[:,7:].apply(lambda x: x.index[x.astype(bool)].tolist(), 1)
        p,n,lun=[],[],[]
        for i in list(range(df.shape[0])):
            for l in df.iloc[i, 18]:
                p.append(l)
                n.append(df.iloc[i, 0])
                lun.append(len(df.iloc[i, 18]))
        riep=pd.DataFrame({'Pos':p,'N':n,'Len':lun})
        f2=pd.merge(riep,df.iloc[:,:7],left_on='N',right_on='Nome',how='left')
        f2=f2.drop('N',axis=1).drop('Len',axis=1).sort_values('FV',ascending=False)
        Bsel=pd.merge(f2,f2.groupby('Pos',as_index=False).agg({'FV':'max','Nome':'first'}),on=['Pos','FV','Nome'],how='right')
        Bsel['ID']=[x+y for x,y in zip(Bsel['Pos'],Bsel['Nome'])]
        f2['ID']=[x+y for x,y in zip(f2['Pos'],f2['Nome'])]
        sub=f2[~f2['ID'].isin(Bsel['ID'])]
        while Bsel.shape[0]<11:
            Bsel.loc[Bsel.shape[0]]=['','','',0,g,s,'',Bsel.iloc[0,7],'']
        count_dup = sum(pd.value_counts(list(filter(None,Bsel['Nome']))).to_frame().reset_index()[0]!=1)
        while count_dup!=0:
            for nn in list(filter(None,list(set(Bsel['Nome'])))):
                h=Bsel[Bsel['Nome']==nn].shape[0]
                while h>1:
                    selec=sub[sub['Pos'].isin(Bsel.loc[Bsel['Nome']==nn,'Pos'])].head(1)
                    if selec.shape[0]>0:
                        Bsel[Bsel['Pos']==selec.iloc[0,0]]=selec.iloc[0,0],selec.iloc[0,1],selec.iloc[0,2],selec.iloc[0,3],selec.iloc[0,4],selec.iloc[0,5],selec.iloc[0,6],selec.iloc[0,7],selec.iloc[0,8]
                    else:
                        Bsel=Bsel[~Bsel['Pos'].isin(Bsel.loc[Bsel['Nome']==nn,'Pos'].head(1))]
                        Bsel.reset_index(drop=True,inplace=True)
                        Bsel.loc[Bsel.shape[0]]=['','','',0,g,s,'',Bsel.iloc[0,7],'']
                    sub=sub[~sub['ID'].isin(selec['ID'])]
                    h=h-1
            count_dup = sum(pd.value_counts(list(filter(None,Bsel['Nome']))).to_frame().reset_index()[0]!=1)
        f_df=f_df.append(Bsel.iloc[:,:8])
    bmodglob=f_df.groupby('Modulo',as_index=False).agg({'FV':sum}).sort_values(by=['FV'], ascending=False)
    bmod=bmodglob.head(1)
    f_df.sort_index(inplace=True)
    bline=f_df[f_df['Modulo']==int(bmod['Modulo'])]
    bline['Modulo']=[int(x) for x in bline['Modulo']]
    return bline

#controclassifica senza calendario
def controclass(seas):
    db = campionato[campionato['Stagione'] == seas]
    df_riad = pd.DataFrame({'Giornata':list(db['Giornata'])*2,'Team':list(db['Home'])+list(db['Away']),'Gol':list(db['GH'])+list(db['GA'])})
    df_riad = df_riad.sort_values(by=['Giornata', 'Team'])
    exp_points = []
    for gio in list(set(df_riad['Giornata'])):
        df_day = df_riad[df_riad['Giornata'] == gio]
        for squad in df_day['Team']:
            list_gol_xtra_team = list(df_day.loc[df_day['Team'] != squad, 'Gol'])
            gf_team = int(df_day.loc[df_day['Team'] == squad, 'Gol'])
            p_vinte = sum([1 if gf_team > x else 0 for x in list_gol_xtra_team])
            p_pari = sum([1 if gf_team == x else 0 for x in list_gol_xtra_team])
            exp_points.append((p_vinte * 3 + p_pari) / 9)
    df_riad['Exp_Pnt'] = exp_points
    df_cc=df_riad.groupby(['Team'],as_index=False).agg({'Exp_Pnt':'sum'}).sort_values(by=['Exp_Pnt'],ascending=False)
    df_cc['Exp_Pnt']=[int(x) for x in df_cc['Exp_Pnt']]
    return df_cc

def cronistoria(team,comp):
    db=albo_doro[(albo_doro['Squadra']==team) & (albo_doro['Competizione']==comp)]
    if db.shape[0]>0:
        db=db[['Stagione','Risultato']]
    return db

def precedenti(team):
    campionato['WH']=[1 if x>y else 0 for x,y in zip(campionato['GH'],campionato['GA'])]
    campionato['D'] = [1 if x == y else 0 for x,y in zip(campionato['GH'], campionato['GA'])]
    campionato['WA'] = [1 if x < y else 0 for x,y in zip(campionato['GH'], campionato['GA'])]
    db_casa=campionato[campionato['Home']==team]
    db_tras=campionato[campionato['Away']==team]
    db_casa=db_casa[['Away','WH','D','WA','GH','GA','PntH']]
    db_casa.columns=['Avversario','V','N','P','GF','GS','Gio']
    db_tras = db_tras[['Home', 'WA','D','WH', 'GA', 'GH','PntA']]
    db_tras.columns = ['Avversario','V','N','P','GF','GS','Gio']
    db=db_casa.append(db_tras).groupby(['Avversario']).agg({'Gio':'count','V':'sum','N':'sum','P':'sum','GF':'sum','GS':'sum'})
    db['Bilancio']=[x-y for x,y in zip(db['V'],db['P'])]
    return db.sort_values(by=['Bilancio'],ascending=False)

def player_cards(squad):
    list_img = []
    name_font = requests.get('http://themes.googleusercontent.com/static/fonts/racingsansone/v1/1r3DpWaCiT7y3PD4KgkNyO921tOcMok2fHawGmtxikA.ttf')
    font_all = requests.get('http://themes.googleusercontent.com/static/fonts/robotoslab/v2/y7lebkjgREBJK96VQi37Zp0EAVxt0G0biEntp43Qt6E.ttf')
    for i in list(range(squad.shape[0])):
        cart = Image.open(BytesIO(requests.get(load_images_cup()[5]).content))
        if pd.notnull(squad.iloc[i,9]):
            play = Image.open(BytesIO(requests.get(squad.iloc[i,9]).content))
            pl_resz = play.resize((200, 300))
            cart.paste(pl_resz, (440, 140))
        img_drw = ImageDraw.Draw(cart)
        bigFont = ImageFont.truetype(BytesIO(font_all.content),40)
        mediumFont = ImageFont.truetype(BytesIO(font_all.content),30)
        smallFont = ImageFont.truetype(BytesIO(font_all.content),20)
        xsmallFont = ImageFont.truetype(BytesIO(font_all.content),15)
        nf = ImageFont.truetype(BytesIO(name_font.content),30)
        img_drw.text((245, 200), str(squad.iloc[i,4]), font=bigFont, fill=(0, 0, 0))
        if len(squad.iloc[i,5].split(";"))==1:
            img_drw.text((245, 300), str(squad.iloc[i,5]), font=mediumFont, fill=(0, 0, 0))
        elif len(squad.iloc[i,5].split(";"))==2:
            img_drw.text((235, 300), str(squad.iloc[i, 5]), font=mediumFont, fill=(0, 0, 0))
        else:
            img_drw.text((225, 300), str(squad.iloc[i, 5]), font=mediumFont, fill=(0, 0, 0))
        img_drw.text((260, 520), str(squad.iloc[i, 0]), font=nf, fill=(0, 0, 0))
        img_drw.text((260, 580), str(squad.iloc[i, 1]), font=smallFont, fill=(0, 0, 0))
        img_drw.text((260, 620), str(squad.iloc[i, 2]), font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((260, 660), str(squad.iloc[i, 3]), font=smallFont, fill=(0, 0, 0))
        img_drw.text((260, 700), str(squad.iloc[i, 7]), font=smallFont, fill=(0, 0, 0))
        img_drw.text((300, 740), str(squad.iloc[i, 8]), font=smallFont, fill=(0, 0, 0))

        img_drw.text((350, 220), "Età", font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((350, 320), "Ruolo", font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((500, 580), "Data nascita", font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((500, 620), "Luogo nascita", font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((500, 660), "Nazionalità", font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((500, 700), "Scadenza", font=xsmallFont, fill=(0, 0, 0))
        img_drw.text((500, 740), "Indennizzo", font=xsmallFont, fill=(0, 0, 0))
        list_img.append(cart.convert('RGBA'))
    return list_img