from __future__ import annotations
import streamlit as st
from src.translations import t,region_name,risk_name
from components.ui import page_header,kpi,section,footnote,show_chart
from components.charts import regional_bars,year_comparison
from src.maps import reference_map,LABEL_ANCHORS


def render():
    rain=st.session_state['rain']; year=int(st.session_state['year']); default_region=st.session_state['region']
    page_header(t('atlas_title'),t('atlas_desc'))
    a,b=st.columns([1.8,1],gap='large')
    with a:
        selected=st.selectbox(t('map_selected'),list(LABEL_ANCHORS),index=list(LABEL_ANCHORS).index(default_region) if default_region in LABEL_ANCHORS else 0,format_func=region_name,key='atlas_region')
        show_chart(reference_map(rain,year,names=region_name,selected=selected))
        st.caption(t('outline_notice'))
    with b:
        st.write('')
        section(f'{region_name(selected)} · {year}')
        row=rain[(rain.region==selected)&(rain.year==year)].iloc[0]
        kpi(t('observed'),f'{row.JJAS:.1f} mm',t('historic_only'))
        st.write('')
        kpi(t('anomaly'),f'{row.anomaly_pct:+.1f}%',risk_name(row.rainfall_class))
        st.write('')
        kpi(t('reference'),f'{row.reference_mm:.1f} mm','1871–1995')
        st.caption(t('map_legend'))
    st.divider()
    l,r=st.columns([1.13,1],gap='large')
    with l:
        section(t('compare_regions'))
        show_chart(regional_bars(rain,year,names=region_name))
    with r:
        section(t('year_compare'))
        other=st.select_slider(t('compare_year'),options=list(range(1871,2017)),value=1999,key='atlas_compare_year')
        show_chart(year_comparison(rain[rain.region==selected],[year,other]))
    footnote(t('outline_notice'))
