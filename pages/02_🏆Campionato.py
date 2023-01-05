from funzioni import *

st.title("Stats Campionato")
sel_sea=st.selectbox('Scegli una stagione:',tuple(sorted(set(campionato['Stagione']))))

tab6, tab7, tab8, tab9 = st.tabs(["Classifiche stagionali","Classifica perpetua","Money","Top11"])
with tab6:
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
    with st.expander("Gap bilancio/soglia default"):
        b=billato(seas=sel_sea)
        b=b.groupby(['Squadra'],as_index=False).agg({'Tot':'sum'})
        cla = ranking(seas=sel_sea)
        soglie=deco_prizes[deco_prizes['Stagione']==sel_sea]
        b_cla=pd.merge(b,cla[['Pos','Squadra']],on='Squadra',how='left')
        b_cla_s=pd.merge(b_cla,soglie[['Pos','Soglia']],on='Pos',how='left')
        a_chart = go.Figure()
        a_chart.add_trace(go.Scatter(x=b_cla_s['Squadra'], y=b_cla_s['Soglia'], fill='tozeroy', name="Soglia"))
        a_chart.add_trace(go.Scatter(x=b_cla_s['Squadra'], y=b_cla_s['Tot'], fill='tonexty', name='Bilancio'))
        a_chart.update_layout(legend=dict(orientation="h",y=1.1))
        st.plotly_chart(a_chart, use_container_width=True)
    with st.expander("Andamento monte stipendi per giornata"):
        v_stip = voti_arricchiti()[voti_arricchiti()['Stagione']==sel_sea]
        vs=v_stip.groupby(['Giornata','Squadra'],as_index=False).agg({'Stipendio':'sum'})
        s_chart = go.Figure()
        for gio in set(vs['Giornata']):
            v_temp=vs[vs['Giornata']==gio]
            for i in list(range(v_temp.shape[0])):
                s_chart.add_trace(go.Bar(y=[v_temp.iloc[i,2]], x=[gio],name=v_temp.iloc[i,1],orientation='v'))
        s_chart.update_layout(barmode='relative', showlegend=False)
        st.plotly_chart(s_chart, use_container_width=True)
with tab9:
    vb = voti_arricchiti()[voti_arricchiti()['Stagione']==sel_sea]
    gg = st.slider('Scegli una giornata (di serie A):',min_value=3, max_value=max(vb['Giornata']), value=max(vb['Giornata']))

    best11=b11(seas=sel_sea,gio=gg)
    b11pos=pd.merge(best11,grafica,on=['Modulo','Pos'],how='left')
    b11_chart = go.Figure()
    b11_chart.add_trace(go.Scatter(y=b11pos['y'],x=b11pos['x'],mode='markers+text',marker_color='blue',
                                   text=['<b>'+str(x)+'<b> <br> <b>'+str(y)+'<b>' for x,y in zip(b11pos['Nome'],b11pos['FV'])],textposition='bottom center',textfont_color='black'))
    b11_chart.update_traces(mode='markers+text', marker_line_width=2, marker_size=10)
    b11_chart.add_layout_image(dict(source=Image.open(BytesIO(requests.get(load_images_cup()[4]).content)),
                               layer="below",sizing='stretch',opacity=0.7,x=0,y=1,xanchor='left',yanchor='top',sizex=1,sizey=1))
    b11_chart.update_xaxes(showgrid=False,zeroline=False,visible=False)
    b11_chart.update_yaxes(showgrid=False, zeroline=False,visible=False)
    col16, col17 = st.columns(2)
    with col16:
        st.write("Best 11 di giornata")
        st.plotly_chart(b11_chart, use_container_width=True)
    with col17:
        st.metric("Modulo",max(best11['Modulo']))
        st.metric("Punti totali", sum(best11['FV']))


