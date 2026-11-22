from __future__ import annotations
import streamlit as st
from src.translations import t,region_name,risk_name
from src.data import REGIONS
from components.ui import page_header,kpi,section,footnote,show_chart
from components.charts import rainfall_trend,month_profile,anomaly_heatmap


def render():
    data=st.session_state['rain']; region=st.session_state['region']
    page_header(t('history'),t('since'))
    c1,c2=st.columns(2)
    with c1: start=st.number_input(t('from_year'),min_value=1871,max_value=2015,value=1950,key='hist_start',step=1)
    with c2: end=st.number_input(t('to_year'),min_value=1872,max_value=2016,value=2016,key='hist_end',step=1)
    if start>=end:
        st.warning('Start year must be earlier than end year.' if st.session_state.lang=='en' else 'शुरू वर्ष अंतिम वर्ष से पहले होना चाहिए।');return
    part=data[(data.region==region)&data.year.between(start,end)].copy()
    row=data[data.region==region]
    low=part.loc[part.anomaly_pct.idxmin()]; high=part.loc[part.anomaly_pct.idxmax()]
    a,b,c=st.columns(3)
    with a:kpi(t('mean'),f'{row.reference_mm.iloc[0]:.1f} mm','1871–1995')
    with b:kpi(t('minimum'),f'{low.anomaly_pct:+.1f}%',str(int(low.year)))
    with c:kpi(t('maximum'),f'{high.anomaly_pct:+.1f}%',str(int(high.year)))
    st.write('');section(t('trend'))
    show_chart(rainfall_trend(part))
    a,b=st.columns([1.04,1],gap='large')
    with a:
        section(t('monthly_pattern'))
        show_chart(month_profile(part))
    with b:
        section(t('top_dry'))
        dry=part.nsmallest(6,'anomaly_pct')[['year','JJAS','anomaly_pct','rainfall_class']].copy()
        dry.rainfall_class=dry.rainfall_class.map(risk_name)
        st.dataframe(dry.rename(columns={'year':t('year'),'JJAS':t('observed'),'anomaly_pct':t('anomaly'),'rainfall_class':t('category')}),hide_index=True,use_container_width=True)
        section(t('top_wet'))
        wet=part.nlargest(4,'anomaly_pct')[['year','JJAS','anomaly_pct']]
        st.dataframe(wet.rename(columns={'year':t('year'),'JJAS':t('observed'),'anomaly_pct':t('anomaly')}),hide_index=True,use_container_width=True)
    section(t('heatmap'))
    show_chart(anomaly_heatmap(data,[r for r in REGIONS if r!='All India'],start,end,names=region_name))
    st.download_button(t('download_data'),part.to_csv(index=False).encode('utf-8-sig'),file_name=f'historical_{region.lower().replace(" ","_")}_{start}_{end}.csv',mime='text/csv')
    footnote(t('classification_notice'))
