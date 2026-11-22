"""Vṛṣṭi-Vijñāna | bilingual, offline, 7-page monsoon intelligence demonstration.
Run from project directory: python -m streamlit run app.py
"""
from __future__ import annotations
import streamlit as st
from src.data import REGIONS,annual_with_anomaly,load_rainfall,load_rules
from src.models import build_results
from src.translations import t,region_name
from components.ui import apply_css,footnote
from pages import (dashboard,monsoon_atlas,historical_analysis,ai_model_lab,
                   traditional_knowledge,insights_reports,methodology)

st.set_page_config(page_title='Vṛṣṭi-Vijñāna | Monsoon Intelligence',page_icon='🌧️',layout='wide',initial_sidebar_state='expanded')
apply_css()

@st.cache_data(show_spinner=False)
def cached_data():
    return annual_with_anomaly(load_rainfall()),load_rules()

@st.cache_resource(show_spinner='Evaluating historical rainfall models…')
def cached_models():
    return build_results(load_rainfall())

# Initialise in the router, not in each page; state persists while navigating.
if 'lang' not in st.session_state:st.session_state.lang='en'
if 'year' not in st.session_state:st.session_state.year=2002
if 'region' not in st.session_state:st.session_state.region='Northwest India'

rain,rules=cached_data()
preds,scores,trained=cached_models()
for key,val in {'rain':rain,'rules':rules,'predictions':preds,'scores':scores,'trained':trained}.items():
    st.session_state[key]=val

with st.sidebar:
    st.markdown('<div class="brand">◈ Vṛṣṭi-Vijñāna</div><div class="brand-sub">MONSOON INTELLIGENCE PLATFORM</div>',unsafe_allow_html=True)
    st.caption(t('hackathon'))
    st.selectbox('Language / भाषा',['en','hi'],format_func=lambda x:'English' if x=='en' else 'हिन्दी',key='lang')
    st.divider()
    st.markdown('**'+t('year')+'**')
    st.select_slider(t('year'),options=list(range(1871,2017)),key='year',label_visibility='collapsed')
    st.markdown('**'+t('region')+'**')
    st.selectbox(t('region'),REGIONS,format_func=region_name,key='region',label_visibility='collapsed')
    st.divider()
    st.caption(t('disclaimer'))

pages=[
    st.Page(dashboard.render,title=t('dashboard'),icon=':material/space_dashboard:',url_path='dashboard',default=True),
    st.Page(monsoon_atlas.render,title=t('atlas'),icon=':material/public:',url_path='monsoon-atlas'),
    st.Page(historical_analysis.render,title=t('history'),icon=':material/show_chart:',url_path='history'),
    st.Page(ai_model_lab.render,title=t('models'),icon=':material/model_training:',url_path='model-lab'),
    st.Page(traditional_knowledge.render,title=t('knowledge'),icon=':material/menu_book:',url_path='traditional-knowledge'),
    st.Page(insights_reports.render,title=t('insights'),icon=':material/description:',url_path='insights-reports'),
    st.Page(methodology.render,title=t('method'),icon=':material/verified:',url_path='methodology'),
]
selected=st.navigation(pages,position='sidebar')
selected.run()
