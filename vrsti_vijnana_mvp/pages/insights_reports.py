from __future__ import annotations
import streamlit as st
from src.translations import t,region_name,risk_name
from src.reports import report_markdown
from components.ui import page_header,kpi,section,footnote


def render():
    data=st.session_state['rain']; year=int(st.session_state['year']); region=st.session_state['region']
    page_header(t('report_title'),t('report_desc'))
    row=data[(data.year==year)&(data.region==region)].iloc[0]
    a,b,c=st.columns(3)
    with a:kpi(t('observed'),f'{row.JJAS:.1f} mm',f'{region_name(region)}, {year}')
    with b:kpi(t('anomaly'),f'{row.anomaly_pct:+.1f}%','1871–1995')
    with c:kpi(t('category'),risk_name(row.rainfall_class),t('historic_only'))
    st.write('');section(t('interpretation'))
    anom=float(row.anomaly_pct)
    if st.session_state.lang=='hi':
        msg='इस वर्ष दर्ज वर्षा ऐतिहासिक औसत से कम रही।' if anom < -10 else ('इस वर्ष दर्ज वर्षा ऐतिहासिक औसत से अधिक रही।' if anom > 10 else 'इस वर्ष दर्ज वर्षा ऐतिहासिक औसत के आसपास रही।')
    else:
        msg='Observed rainfall was below the historical reference.' if anom < -10 else ('Observed rainfall was above the historical reference.' if anom > 10 else 'Observed rainfall was near the historical reference.')
    st.info(msg+' '+t('historical'))
    section(t('impact'))
    st.write(t('impact_hint'))
    st.divider()
    section(t('preview'))
    report=report_markdown(row,st.session_state.lang)
    with st.expander(t('preview'),expanded=True):
        st.markdown(report)
    l,r=st.columns(2)
    with l:st.download_button(t('download_report'),report.encode('utf-8'),file_name=f'vrsti_{region.lower().replace(" ","_")}_{year}_{st.session_state.lang}.md',mime='text/markdown',use_container_width=True)
    with r:
        history=data[(data.region==region)&(data.year<=year)][['year','JJAS','reference_mm','anomaly_pct','rainfall_class']]
        st.download_button(t('download_data'),history.to_csv(index=False).encode('utf-8-sig'),file_name=f'vrsti_{region.lower().replace(" ","_")}_history.csv',mime='text/csv',use_container_width=True)
    footnote(t('classification_notice'))
