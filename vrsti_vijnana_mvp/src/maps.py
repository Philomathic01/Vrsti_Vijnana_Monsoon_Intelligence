"""Offline reference map. Rainfall regions do not have verified vector boundaries.
Markers are illustrative label anchors, never model grid points or polygons.
"""
from __future__ import annotations
import json
from pathlib import Path
import plotly.graph_objects as go
from components.charts import stylize
from src.translations import t
from components.ui import RED,TEAL,BLUE,AMBER,INK

ROOT=Path(__file__).resolve().parents[1]
# Representative anchor coordinates for *labels* only. NOT measurements or regional centroids.
LABEL_ANCHORS={
 'Northwest India':(74.0,28.7),
 'West Central India':(76.1,23.1),
 'Northeast India':(92.0,26.0),
 'Central Northeast India':(83.2,25.6),
 'Peninsular India':(78.9,14.0),
}

def reference_map(data,year:int,names=lambda x:x,selected='Northwest India',title=None):
    feat=json.loads((ROOT/'assets'/'india_outline.geojson').read_text(encoding='utf-8'))
    geom=feat['geometry']; poly=geom['coordinates']
    outer_rings=[p[0] for p in poly] if geom['type']=='MultiPolygon' else [poly[0]]
    fig=go.Figure()
    for ring in outer_rings:
        # reference country outline only; not authoritative international or regional boundary
        lon=[p[0] for p in ring]; lat=[p[1] for p in ring]
        fig.add_trace(go.Scatter(x=lon,y=lat,fill='toself',mode='lines',line=dict(color='#4D9097',width=1.7),
            fillcolor='#173B4E',hoverinfo='skip',showlegend=False))
    selected_rows=data[(data.year==year)&data.region.isin(LABEL_ANCHORS)].set_index('region')
    for region,(lon,lat) in LABEL_ANCHORS.items():
        row=selected_rows.loc[region]
        deviation=float(row.anomaly_pct)
        c= RED if deviation < -10 else BLUE if deviation > 10 else TEAL
        focus=region==selected
        fig.add_trace(go.Scatter(x=[lon],y=[lat],mode='markers+text',
          marker=dict(color=c,size=24 if focus else 17,line=dict(color='#E7FAFF' if focus else '#123448',width=2 if focus else 1)),
          text=[names(region)],textposition='top center',textfont=dict(size=12 if focus else 10,color='#FFFFFF' if focus else '#BCD7E1'),
          name=names(region),showlegend=False,
          customdata=[[float(row.JJAS),float(row.reference_mm),deviation]],
          hovertemplate=f'<b>{names(region)}</b><br>{year} · {t("observed")}: %{{customdata[0]:.1f}} mm<br>{t("reference")}: %{{customdata[1]:.1f}} mm<br>{t("anomaly")}: %{{customdata[2]:+.1f}}%<extra></extra>'))
    fig.update_xaxes(visible=False,range=[66.0,100.2],scaleanchor='y',scaleratio=1,showgrid=False)
    fig.update_yaxes(visible=False,range=[6.3,37.5],showgrid=False)
    fig.update_layout(hovermode='closest',dragmode='pan',margin=dict(l=8,r=12,t=52 if title else 15,b=10))
    return stylize(fig,title,550,legend=False)
