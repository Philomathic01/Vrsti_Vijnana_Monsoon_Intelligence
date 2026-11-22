"""Shared visual components for dark editorial climate-tech Streamlit UI."""
from html import escape
import streamlit as st
from src.translations import t

INK='#EAF9F5'; MUTED='#9DBAC5'; TEAL='#28D7B3'; BLUE='#5AB9F6'; RED='#FF777B'; AMBER='#F5C46A'
RISK_COLOURS={'Below normal':RED,'Near normal':TEAL,'Above normal':BLUE}
CSS='''
<style>
:root{color-scheme:dark}
.stApp{background:radial-gradient(ellipse at 90% 5%,#133C4E 0,transparent 27%),linear-gradient(135deg,#061624,#0A2431 62%,#092934);color:#EAF9F5}
html,body,[data-testid="stApp"]{font-family:Inter,Arial,sans-serif}
section[data-testid="stSidebar"]{background:#081D2B;border-right:1px solid #214252}
[data-testid="stSidebarNav"]{margin-top:16px}
.block-container{max-width:1440px;padding:1.4rem 2rem 2.8rem}
h1,h2,h3{letter-spacing:-.025em;color:#F4FFFB!important}
h1{font-weight:800!important}
h2{font-weight:760!important}
[data-testid="stMetric"]{background:#102E3E;border:1px solid #225266;border-radius:16px;padding:18px 21px}
[data-testid="stMetricLabel"]{color:#B5D1D6!important}
[data-testid="stMetricValue"]{color:#FAFFFB!important;font-weight:750!important}
[data-testid="stMetricDelta"]{color:#A0CED6!important}
[data-testid="stDataFrame"], .stAlert{border-radius:14px!important}
div.stButton>button[kind="primary"]{background:linear-gradient(100deg,#19D7B1,#4CCDBC);color:#062329;font-weight:750;border:0}
div.stDownloadButton>button{border-color:#2E6870!important;border-radius:11px!important}
.hero{position:relative;overflow:hidden;background:radial-gradient(circle at 100% 0%,#1C806E55,transparent 45%),linear-gradient(115deg,#114453,#102B43 66%,#0D2940);border:1px solid #326A74;border-radius:25px;padding:32px 36px 29px;margin-bottom:17px}
.hero:after{content:'◌';position:absolute;font-size:240px;top:-100px;right:20px;color:#63F5C9;opacity:.13;pointer-events:none}
.eyebrow{font-size:.73rem;letter-spacing:.16em;text-transform:uppercase;color:#80F1D1;font-weight:800;margin-bottom:9px}
.hero h1{font-size:clamp(1.7rem,3.2vw,2.8rem);line-height:1.13;margin:0 0 12px}
.hero p{font-size:.98rem;line-height:1.6;color:#BCD8DD;max-width:780px;margin:0}
.pill{display:inline-flex;align-items:center;gap:6px;border:1px solid #32847D;background:#124F4B;padding:6px 12px;color:#BEFFDD;border-radius:30px;font-size:.75rem;font-weight:700;margin:17px 9px 0 0}
.kpi{background:linear-gradient(135deg,#143749,#102B3B);border:1px solid #255467;border-radius:16px;padding:18px 21px;min-height:115px}
.kpi .klabel{color:#B4D2D8;font-size:.78rem}
.kpi .kvalue{font-size:1.65rem;letter-spacing:-.02em;font-weight:800;color:#F7FFFC;margin:5px 0}
.kpi .kfoot{color:#9BB9C5;font-size:.72rem}
.paneltitle{font-size:1.02rem;font-weight:780;color:#EBFAF6;padding:3px 0 8px}
.disclaimer{border:1px solid #4A5047;background:#303C40;border-radius:11px;padding:12px 16px;color:#EDD9A9;font-size:.79rem;line-height:1.65;margin-top:15px}
.statustag{display:inline-block;padding:5px 10px;border-radius:30px;background:#174B4A;border:1px solid #2F7B78;color:#A6F6D1;font-size:.77rem;font-weight:700}
.brand{font-size:1.27rem;font-weight:850;color:#EEFFF9;line-height:1.4}
.brand-sub{font-size:.69rem;letter-spacing:.12em;font-weight:750;color:#86D5C9;margin-bottom:16px}
footer{visibility:hidden}
@media(max-width:750px){.block-container{padding:1.0rem .8rem 2rem}.hero{padding:23px 21px}.kpi{min-height:97px;padding:13px}}
</style>
'''

def apply_css(): st.markdown(CSS,unsafe_allow_html=True)

def hero(title,description,eyebrow=None,pills=()):
    p=''.join('<span class="pill">'+escape(str(x))+'</span>' for x in pills)
    st.markdown(f'<div class="hero"><div class="eyebrow">{escape(eyebrow or t("hero_eyebrow"))}</div>'
                f'<h1>{escape(title)}</h1><p>{escape(description)}</p>{p}</div>',unsafe_allow_html=True)

def page_header(title,subtitle,eyebrow=None): hero(title,subtitle,eyebrow,())

def kpi(label,value,foot=''):
    st.markdown(f'<div class="kpi"><div class="klabel">{escape(str(label))}</div>'
                f'<div class="kvalue">{escape(str(value))}</div><div class="kfoot">{escape(str(foot))}</div></div>',unsafe_allow_html=True)

def section(title): st.markdown(f'<div class="paneltitle">{escape(title)}</div>',unsafe_allow_html=True)

def footnote(extra=''):
    st.markdown(f'<div class="disclaimer">{escape(t("disclaimer"))}'+ (f' · {escape(extra)}' if extra else '') +'</div>',unsafe_allow_html=True)

def show_chart(fig, height=None):
    if height: fig.update_layout(height=height)
    st.plotly_chart(fig,use_container_width=True,config={'displaylogo':False,'scrollZoom':False,'toImageButtonOptions':{'format':'png','scale':2}})
