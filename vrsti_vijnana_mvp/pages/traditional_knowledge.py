from __future__ import annotations
import streamlit as st
from src.translations import t
from components.ui import page_header,kpi,section,footnote


def render():
    rules=st.session_state['rules']
    page_header(t('knowledge'),t('rules_intro'))
    c1,c2,c3=st.columns([1.1,1.3,1.5])
    with c1:
        opts=[t('all_categories')]+sorted(rules['Method Category'].unique().tolist())
        category=st.selectbox(t('category_filter'),opts,key='tek_category')
    first=rules if category==t('all_categories') else rules[rules['Method Category']==category]
    with c2:
        subopts=[t('all_subcategories')]+sorted(first['Method Sub-Category'].unique().tolist())
        sub=st.selectbox(t('subcategory_filter'),subopts,key='tek_sub')
    with c3:
        query=st.text_input(t('search_rule'),placeholder='nakshatra / cloud / wind / rain',key='tek_query')
    filtered=first if sub==t('all_subcategories') else first[first['Method Sub-Category']==sub]
    if query.strip():
        # Search only supplied metadata/text fields; no machine translation of claimed rules.
        mask=filtered.apply(lambda row: query.casefold() in ' '.join(map(str,row.values)).casefold(),axis=1)
        filtered=filtered[mask]
    a,b,c=st.columns(3)
    with a:kpi(t('rules'),len(rules),t('reference_warning'))
    with b:kpi(t('available'),len(filtered),t('status'))
    with c:kpi(t('not_validated'),len(rules),t('research'))
    st.write('')
    if filtered.empty:
        st.info(t('no_matches'));return
    choices=filtered['Rule ID'].tolist()
    item=st.selectbox(t('rule_selector'),choices,format_func=lambda key:
      key+' · '+str(filtered.loc[filtered['Rule ID']==key,'Criteria'].iloc[0])[:75],key='tek_pick')
    row=filtered[filtered['Rule ID']==item].iloc[0]
    st.write('')
    left,right=st.columns([1.25,1],gap='large')
    with left:
        st.markdown(f'#### {row["Rule ID"]} · {row["Method Category"]}')
        st.markdown(f'**{t("criteria")}**')
        st.write(str(row['Criteria']))
        st.markdown(f'**{t("claimed")}**')
        st.write(str(row['Result']))
        st.markdown(f'**{t("source")}**')
        st.write(str(row['Source Text']))
        if str(row['Verse Number']):
            st.caption(f'Verse number as supplied: {row["Verse Number"]}')
        with st.expander(t('original_source'),expanded=True):
            st.write(str(row['Verse']) if str(row['Verse']) else '—')
    with right:
        st.warning(t('not_validated'))
        section(t('test_plan'))
        st.write(t('tek_plan'))
        with st.expander('Extra notes / अतिरिक्त नोट',expanded=False):
            st.write(str(row['Extra Note']) if str(row['Extra Note']) else '—')
        st.caption(t('reference_warning'))
    st.divider()
    section(t('data_download'))
    st.download_button(t('download_data'),filtered.to_csv(index=False).encode('utf-8-sig'),
                       'traditional_knowledge_rules.csv',mime='text/csv')
    footnote(t('not_validated'))
