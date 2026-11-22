from __future__ import annotations
import streamlit as st
from src.translations import t,region_name,risk_name
from components.ui import hero,kpi,section,footnote,show_chart
from components.charts import regional_bars,rainfall_trend


def render():
    rain=st.session_state['rain']; rules=st.session_state['rules']
    year=int(st.session_state['year']); region=st.session_state['region']
    observation=rain[(rain.year==year)&(rain.region==region)].iloc[0]
    hero(t('hero_title'),t('hero_desc'),pills=(t('since'),t('hackathon')))
    cols=st.columns(4,gap='medium')
    cards=[(t('records'),f'{len(rain):,}',t('since')),
           (t('regions'),str(rain.region.nunique()),'5 + All-India'),
           (t('rules'),str(len(rules)),t('not_validated')),
           (t('anomaly'),f'{observation.anomaly_pct:+.1f}%',f'{region_name(region)} · {year}')]
    for col,(label,val,foot) in zip(cols,cards):
        with col:kpi(label,val,foot)
    st.write('')
    left,right=st.columns([1.14,1],gap='large')
    with left:
        section(f'{t("snapshot")} · {year}')
        vals=rain[(rain.year==year)]
        show_chart(regional_bars(vals,year,names=region_name))
    with right:
        section(f'{region_name(region)} · {t("trend")}')
        part=rain[rain.region==region]
        show_chart(rainfall_trend(part))
    ai=rain[(rain.year==year)&(rain.region=='All India')].iloc[0]
    st.info(f'{t("fact")}: {year} · {region_name("All India")} {ai.anomaly_pct:+.1f}% | '
            f'{region_name("Northwest India")}: {rain[(rain.year==year)&(rain.region=="Northwest India")].iloc[0].anomaly_pct:+.1f}%. '
            f'{t("historical")}')
    section(t('compare_regions'))
    region_rows=rain[(rain.year==year)&(rain.region!='All India')][['region','JJAS','reference_mm','anomaly_pct','rainfall_class']].copy()
    region_rows['region']=region_rows['region'].map(region_name)
    region_rows['rainfall_class']=region_rows['rainfall_class'].map(risk_name)
    st.dataframe(region_rows.rename(columns={'region':t('region'),'JJAS':t('observed'),'reference_mm':t('reference'),
        'anomaly_pct':t('anomaly'),'rainfall_class':t('category')}),hide_index=True,use_container_width=True)
    footnote(t('classes'))
