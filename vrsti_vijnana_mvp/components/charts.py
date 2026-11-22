"""Plotly chart builders. No streamlit widgets; can be tested without a UI server."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.data import REGIONS,MONTHS
from src.translations import t
from components.ui import TEAL,BLUE,RED,AMBER,INK,MUTED,RISK_COLOURS

SERIES_COLORS={'Climatology':AMBER,'Persistence':RED,'Ridge ML':TEAL,'Random Forest ML':BLUE}

def stylize(fig,title=None,height=370,legend=True):
    fig.update_layout(template='plotly_dark',height=height,
       paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
       font=dict(family='Inter, Arial',size=12,color=INK),
       margin=dict(l=8,r=12,t=60 if title else 25,b=25),
       title=dict(text=title,font=dict(size=17,color=INK),x=.02) if title else None,
       hoverlabel=dict(bgcolor='#123749',font_size=12),
       legend=dict(orientation='h',yanchor='bottom',y=1.01,xanchor='right',x=1) if legend else dict(visible=False),
       xaxis=dict(gridcolor='rgba(177,213,226,.11)',zeroline=False),
       yaxis=dict(gridcolor='rgba(177,213,226,.11)',zeroline=False))
    return fig

def regional_bars(frame, year, names=lambda x:x, title=None):
    d=frame[(frame.year==year)&(frame.region!='All India')].copy()
    d['display']=d.region.map(names)
    d=d.sort_values('anomaly_pct')
    color=[RED if x < -10 else BLUE if x > 10 else TEAL for x in d.anomaly_pct]
    fig=go.Figure(go.Bar(x=d.anomaly_pct,y=d.display,orientation='h',marker_color=color,
      customdata=np.stack([d.JJAS,d.reference_mm],axis=1),
      hovertemplate='%{y}<br>Rainfall anomaly: %{x:+.1f}%<br>Observed: %{customdata[0]:.1f} mm<br>Reference: %{customdata[1]:.1f} mm<extra></extra>'))
    fig.add_vline(x=0,line_color='#93AAB4',line_width=1)
    fig.update_xaxes(title_text=t('anomaly')+' (%)',ticksuffix='%')
    fig.update_layout(yaxis=dict(autorange='reversed',automargin=True),bargap=.36)
    return stylize(fig,title,height=365,legend=False)

def rainfall_trend(part,title=None):
    df=part.sort_values('year')
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df.year,y=df.JJAS,mode='lines',name=t('observed'),line=dict(color=TEAL,width=2),hovertemplate='%{x}: %{y:.1f} mm<extra></extra>'))
    fig.add_trace(go.Scatter(x=df.year,y=df.JJAS.rolling(11,center=True,min_periods=6).mean(),mode='lines',name=t('rolling'),line=dict(color=BLUE,width=3)))
    fig.add_hline(y=float(df.reference_mm.iloc[0]),line_color=AMBER,line_dash='dot',annotation_text=t('reference')+' 1871–1995',annotation_position='top left')
    fig.update_yaxes(title_text=t('rain_unit'))
    fig.update_xaxes(title_text=t('year'))
    return stylize(fig,title,385)

def month_profile(part,title=None):
    vals=part[MONTHS].mean()
    colors=[BLUE if name in ('JUN','JUL','AUG','SEP') else '#2A7881' for name in MONTHS]
    fig=go.Figure(go.Bar(x=MONTHS,y=vals,marker_color=colors,hovertemplate='%{x}: %{y:.1f} mm<extra></extra>'))
    fig.update_yaxes(title_text=t('rain_unit'))
    return stylize(fig,title,330,legend=False)

def anomaly_heatmap(frame,regions=None,start=1950,end=2016,title=None,names=lambda x:x):
    regions=regions or [r for r in REGIONS if r!='All India']
    p=frame[frame.region.isin(regions)&frame.year.between(start,end)].pivot(index='region',columns='year',values='anomaly_pct').reindex(regions)
    fig=go.Figure(go.Heatmap(x=p.columns,y=[names(r) for r in p.index],z=p.values,zmin=-65,zmax=65,zmid=0,
      colorscale=[[0,'#F15E70'],[.5,'#153B48'],[1,'#54A9F2']],colorbar=dict(title=t('anomaly')+' %',thickness=11),
      hovertemplate='%{y}<br>%{x}: %{z:+.1f}%<extra></extra>'))
    fig.update_yaxes(autorange='reversed')
    fig.update_xaxes(title_text=t('year'))
    return stylize(fig,title,340,legend=False)

def model_mae(scores,title=None):
    data=scores.sort_values('mae_mm',ascending=False)
    fig=go.Figure(go.Bar(x=data.mae_mm,y=data.model,orientation='h',marker_color=[SERIES_COLORS[x] for x in data.model],
      text=[f'{v:.1f} mm' for v in data.mae_mm],textposition='outside',cliponaxis=False))
    fig.update_xaxes(title_text=t('best_model')+' (mm)',range=[0,float(data.mae_mm.max())*1.3])
    fig.update_yaxes(automargin=True)
    return stylize(fig,title,320,legend=False)

def hindcasts(part,names,title=None):
    true=part[part.model=='Climatology'].sort_values('year')
    fig=go.Figure(go.Scatter(x=true.year,y=true.observed_mm,mode='lines+markers',name=t('actual'),line=dict(color='#E8F5F5',width=3)))
    for name in names:
        sub=part[part.model==name].sort_values('year')
        fig.add_trace(go.Scatter(x=sub.year,y=sub.predicted_mm,mode='lines+markers',name=name,line=dict(color=SERIES_COLORS[name],width=2),marker=dict(size=5)))
    fig.update_xaxes(dtick=2,title_text=t('year'))
    fig.update_yaxes(title_text=t('rain_unit'))
    return stylize(fig,title,425)

def coefficient_bars(features,coefs,title=None):
    part=pd.DataFrame({'Feature':features,'Coefficient':coefs}).sort_values('Coefficient')
    fig=go.Figure(go.Bar(x=part.Coefficient,y=part.Feature,orientation='h',marker_color=[BLUE if v>=0 else RED for v in part.Coefficient]))
    fig.update_xaxes(title_text=t('coef_unit'))
    return stylize(fig,title,315,legend=False)

def year_comparison(sub,years,title=None):
    d=sub[sub.year.isin(years)].sort_values('year')
    fig=go.Figure(go.Bar(x=d.year.astype(str),y=d.JJAS,marker_color=[TEAL,BLUE],
      text=d.JJAS.map(lambda v:f'{v:.1f} mm'),textposition='outside'))
    fig.add_hline(y=float(d.reference_mm.iloc[0]),line_dash='dot',line_color=AMBER)
    fig.update_yaxes(title_text=t('rain_unit'))
    return stylize(fig,title,310,legend=False)
