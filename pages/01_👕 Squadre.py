import streamlit
from funzioni import *

st.title("Squadre")

list_team=tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan'])))

sel_team=st.selectbox('Scegli una squadra',list_team)

rosa=rosa_oggi(team=sel_team)
rosa['Data nascita']=[x.date() for x in rosa['Data nascita']]
rosa['Indennizzo']=["€{:,.2f}".format(x) for x in rosa['Indennizzo']]

col1, col2 = st.columns(2)
with col1:
    st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[0]).content)))
with col2:
    st.image(Image.open(BytesIO(requests.get(load_images(team=sel_team)[1]).content)))

tab0, \
tab1, tab2, tab3, tab4, tab5 = st.tabs(["La Rosa","Dettaglio rosa","Storico","Insights","Stipendi","Bilancio"])
with tab0:
    with st.expander('Portieri'):
        portie=rosa[rosa['Ruolo']=='Por']
        lp=player_cards(portie)
        for carp in lp:
            st.image(carp)
    with st.expander('Difensori'):
        rdi=ruoli_dif[1:]
        dife=rosa[rosa['Ruolo'].isin(rdi)]
        ld=player_cards(dife)
        for cardi in ld:
            st.image(cardi)
    with st.expander('Centrocampisti'):
        centr=rosa[rosa['Ruolo'].isin(ruoli_cen)]
        lc=player_cards(centr)
        for carc in lc:
            st.image(carc)
    with st.expander('Attaccanti'):
        attc=rosa[rosa['Ruolo'].isin(ruoli_att)]
        la=player_cards(attc)
        for carat in la:
            st.image(carat)
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
    sel_ruolo=st.multiselect("Filtra per ruolo",set([x for x in rosa['Ruolo'] if str(x) != 'nan']),set([x for x in rosa['Ruolo'] if str(x) != 'nan']))
    rosa_short=rosa[['Nome','Ruolo','Età','Contratto','Fine prest','Indennizzo']]
    st.dataframe(rosa_short[rosa_short['Ruolo'].isin(sel_ruolo)])

    with st.expander("Giocatori in prestito"):
        if prestito_players(team=sel_team).shape[0]>0:
            dflp=prestito_players(team=sel_team)
            st.dataframe(dflp)
        else:
            st.write("Nessun giocatore attualmente in prestito")
    with st.expander("Primavera"):
        if primav_players(team=sel_team).shape[0] > 0:
            dfpp = primav_players(team=sel_team)
            st.dataframe(dfpp)
        else:
            st.write("Nessun giocatore attualmente in primavera")
with tab2:
    with st.expander("Palmares e cronistoria"):
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
    with st.expander("Precedenti"):
        st.dataframe(precedenti(team=sel_team))
    with st.expander("Giocatori avversari ispirati"):
        st.write("Top 5 giocatori più odiati dalla squadra:")
        vo = voti_arricchiti_opp()[(voti_arricchiti_opp()['Opponent']==sel_team) & (voti_arricchiti_opp()['Titolarita']==1)]
        vo['Bonus']=[x-y for x,y in zip(vo['FV'],vo['Voto'])]
        ispirati = vo.groupby('Nome',as_index=False).agg({'Bonus':'sum'}).sort_values(by=['Bonus'],ascending=False)
        barisp = go.Figure([go.Bar(x=ispirati.iloc[:5, 1], y=ispirati.iloc[:5, 0], orientation='h')])
        barisp.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(barisp, use_container_width=True)
    with st.expander("Le bandiere"):
        st.write('Numero di giorni in squadra')
        msel=mercato[(mercato['A']==sel_team) & (pd.notnull(mercato['TP']))]
        msel['ddif']=[(x-y).days if x<date.today() else (date.today()-y).days for x,y in zip(msel['TP'],msel['Data'])]
        band=msel.groupby(['Nome'],as_index=False).agg({'ddif':'sum'}).sort_values(by=['ddif'],ascending=False)
        n = st.slider('Numero di bandiere da visualizzare', min_value=1, max_value=10,value=5)
        barband=go.Figure([go.Bar(x=band.iloc[:n,1], y=band.iloc[:n,0],orientation='h')])
        barband.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(barband,use_container_width=True)
with tab3:
    col10, col11 = st.columns(2)
    with col10:
        st.metric("Età media",round(rosa['Età'].mean(),2))
        n_rosa = go.Figure(go.Indicator( domain={'x': [0, 1], 'y': [0, 1]},
            value=rosa.shape[0], mode="gauge+number", title={'text': "Giocatori in rosa"},
            gauge={'axis': {'range': [None, 40]}, 'steps': [
                       {'range': [0, rosa.shape[0]-primav_players(team=sel_team).shape[0]], 'color': "lightgray"},
                       {'range': [rosa.shape[0]-primav_players(team=sel_team).shape[0], rosa.shape[0]], 'color': "gray"}]}))
        st.plotly_chart(n_rosa, use_container_width=True)

        si = sarri_index(team=sel_team)
        si = si.sort_values(by=['Titolarita'], ascending=False).rename({'Titolarita': 'PreFan', 'Voto': 'PreA'})
        st.metric("Sarri Index", np.round(np.var(si['Perc']),3)*100)
        st.write("I più usati")
        st.dataframe(si.head(5))
    with col11:
        st.write('Distribuzione età')
        st.plotly_chart(go.Figure(data=[go.Histogram(x=rosa['Età'],
                                        xbins=dict(start=min(rosa['Età']), end=max(rosa['Età']), size=3))])
                        , use_container_width=True)
        st.write('Distribuzione nazionalità')
        italiani=rosa[rosa['Nazionalità']=='Italia'].shape[0]
        stranieri=rosa[rosa['Nazionalità']!='Italia'].shape[0]
        naz_stra=rosa.loc[rosa['Nazionalità'] != 'Italia','Nazionalità'].value_counts()
        tr1=go.Pie(hole=0.5,sort=False,direction='clockwise',values=[italiani]+naz_stra.tolist(),
                   labels=["Italia"]+naz_stra.index.tolist(),domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]},showlegend=False)
        tr2=go.Pie(hole=0.7,sort=False,direction='clockwise',values=[italiani,stranieri],
                   labels=["Italiani","Stranieri"],textinfo='label',textposition='outside',showlegend=False)
        st.plotly_chart(go.FigureWidget(data=[tr1,tr2]), use_container_width=True)
with tab4:
    col12, col13 = st.columns(2)
    with col12:
        st.write('Monte stip x giornata')
        try:
            db_stip=voti_arricchiti()[(voti_arricchiti()['Squadra']==sel_team) & (voti_arricchiti()['Stagione']==stagione_in_corso)]
            stip_seas=db_stip.groupby(['Giornata']).agg({'Stipendio':'sum'})
            st.line_chart(stip_seas, use_container_width=True)
        except:
            st.info("Stagione non ancora iniziata")
        st.write('Stipendi in campo/panca')
        try:
            stip_seas_ok=sum(db_stip.loc[db_stip['Titolarita']==1,'Stipendio'])
            stip_seas_ko = sum(db_stip.loc[db_stip['Titolarita']==0,'Stipendio'])
            tit_no=go.Pie(hole=0.5,sort=False,direction='clockwise',values=[stip_seas_ok,stip_seas_ko],
                   labels=["Stip in campo","Stip in panca"],showlegend=False)
            st.plotly_chart(go.FigureWidget(data=tit_no), use_container_width=True)
        except:
            st.info("Stagione non ancora iniziata")
    with col13:
        st.write('Top 5 stipendi')
        try:
            stip_player=db_stip.groupby(['Nome'],as_index=False).agg({'Stipendio':'sum'}).sort_values(by=['Stipendio'],ascending=False)
            stip_player['Stipendio'] = ["€{:,.2f}".format(x) for x in stip_player['Stipendio']]
            st.dataframe(stip_player.iloc[:5,:])
        except:
            st.info("Stagione non ancora iniziata")
        st.write('Top 5 lasciati in panchina')
        try:
            non_messi=db_stip[db_stip['Titolarita']==0].sort_values(by=['FV'],ascending=False)
            non_messi=non_messi[['Nome','Giornata','FV']]
            non_messi['FV']=[round(x,2) for x in non_messi['FV']]
            st.dataframe(non_messi.iloc[:5,:])
        except:
            st.info("Stagione non ancora iniziata")
with tab5:
    bil = billato(seas=stagione_in_corso)
    bil = bil[bil['Squadra'] == sel_team]
    spese = bil[bil['Flusso'] == 'Spesa'].sort_values(by=['Tot'])
    entrate = bil[bil['Flusso'] == 'Entrata'].sort_values(by=['Tot'])
    col14, col15 = st.columns(2)
    with col14:
        bil_graph=go.Figure()
        for i in list(range(spese.shape[0])):
            bil_graph.add_trace(go.Bar(y=[-spese.iloc[i,3]], x=["Spese"],name=spese.iloc[i,1],orientation='v'))
        for k in list(range(entrate.shape[0])):
            bil_graph.add_trace(go.Bar(y=[entrate.iloc[k, 3]], x=["Entrate"], name=entrate.iloc[k, 1], orientation='v'))
        bil_graph.update_layout(barmode='relative',showlegend=False)
        st.plotly_chart(go.FigureWidget(data=bil_graph), use_container_width=True)
    with col15:
        st.metric("Bilancio", "€{:,.2f}".format(sum(entrate['Tot'])+sum(spese['Tot'])))
        st.metric("Tot Spese","€{:,.2f}".format(sum(spese['Tot'])))
        st.metric("Tot Entrate", "€{:,.2f}".format(sum(entrate['Tot'])))