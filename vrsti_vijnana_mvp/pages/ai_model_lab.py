from __future__ import annotations
import numpy as np
import streamlit as st
from src.translations import t,region_name,risk_name
from src.data import REGIONS,load_rainfall
from src.models import FEATURES,validation_error_band
from components.charts import model_mae,hindcasts,coefficient_bars,SERIES_COLORS
from components.ui import page_header,kpi,section,footnote,show_chart

MODELS=['Climatology','Persistence','Ridge ML','Random Forest ML']

def render():
    rain=st.session_state['rain']; scores=st.session_state['scores']; preds=st.session_state['predictions']; trained=st.session_state['trained']
    region=st.session_state['region']
    page_header(t('models'),t('model_desc'))
    st.caption(t('holdout'))
    m=scores[scores.region==region].sort_values('mae_mm')
    best=m.iloc[0]
    a,b,c=st.columns(3)
    with a:kpi(t('best_model'),f'{best.mae_mm:.2f} mm',best.model)
    with b:kpi(t('test_years'),'21','1996–2016')
    with c:kpi(t('forecast_cutoff'),t('cutoff_value'),t('historical'))
    st.write(''); l,r=st.columns([.95,1.25],gap='large')
    with l:
        section(t('model_comparison'))
        show_chart(model_mae(m))
    with r:
        section(t('model_comparison')+' · MAE / RMSE / F1')
        st.dataframe(m[['model','mae_mm','rmse_mm','balanced_accuracy','macro_f1']].rename(columns={
           'model':'Model','mae_mm':'MAE (mm)','rmse_mm':'RMSE (mm)','balanced_accuracy':'Balanced accuracy','macro_f1':'Macro-F1'}),hide_index=True,use_container_width=True)
        st.info(t('baseline_note'))
    section(t('hindcast_plot'))
    shown=st.multiselect('Models' if st.session_state.lang=='en' else 'मॉडल',MODELS,default=['Climatology','Ridge ML','Random Forest ML'],key='model_select')
    p=preds[preds.region==region]
    show_chart(hindcasts(p,shown))
    left,right=st.columns([1,1.25],gap='large')
    with left:
        section(t('inspect'))
        year=st.select_slider(t('year'),options=list(range(1996,2017)),value=2002,key='inspect_year')
        choice=st.selectbox(t('chosen_model'),MODELS,index=2,key='inspect_method')
        one=p[(p.year==year)&(p.model==choice)].iloc[0]
        kpi(t('predicted'),f'{one.predicted_mm:.1f} mm',f'{t("actual")}: {one.observed_mm:.1f} mm')
        st.write(''); kpi(t('model_class'),risk_name(one.predicted_class),t('historical'))
        if choice in ('Ridge ML','Random Forest ML'):
            quant=validation_error_band(load_rainfall(),region,choice)
            st.caption((f'Pre-holdout 1981–1995 absolute-error 80th percentile: ±{quant:.1f} mm; not a calibrated prediction interval.'
             if st.session_state.lang=='en' else f'1981–1995 परीक्षण में पूर्ण त्रुटि का 80वाँ प्रतिशतक ±{quant:.1f} मिमी; इसे विश्वसनीय पूर्वानुमान-अंतराल न मानें।'))
    with right:
        section(t('ridge_coeff'))
        ridge=trained[region]['Ridge ML']
        show_chart(coefficient_bars(FEATURES,ridge.named_steps['ridge'].coef_))
        st.caption(t('ridge_note'))
    st.warning(t('missing_climate'))
    st.download_button(t('download_data'),p.to_csv(index=False).encode('utf-8-sig'),
        file_name=f'model_holdout_{region.lower().replace(" ","_")}.csv',mime='text/csv')
    footnote(t('classification_notice'))
