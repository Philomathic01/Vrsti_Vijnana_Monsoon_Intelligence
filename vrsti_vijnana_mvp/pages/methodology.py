from __future__ import annotations
import streamlit as st
from src.translations import t
from components.ui import page_header,section,footnote


def render():
    page_header(t('method_title'),t('method_desc'))
    steps=[(t('methods_data'),t('ready'),
       'Homogeneous regional monthly series, 1871–2016. Six aggregate series, including overlapping All India.'
       if st.session_state.lang=='en' else '1871–2016 की समरूप क्षेत्रीय मासिक वर्षा श्रृंखला; अखिल भारत सहित छह परस्पर समाहित श्रृंखलाएँ।'),
      (t('methods_prep'),t('ready'),
       'Source values are recorded in tenths of millimetres; converted to millimetres. JJAS totals cross-checked against monthly sums.'
       if st.session_state.lang=='en' else 'मूल आँकड़े मिमी के दसवें भाग में थे; मिमी में बदले गए और जून–सितंबर के योग जाँचे गए।'),
      (t('methods_models'),t('ready'),
       'Climatology, persistence, standardized Ridge, and Random Forest; January–May rainfall + previous three JJAS totals.'
       if st.session_state.lang=='en' else 'संदर्भ औसत, पर्सिस्टेंस, रिज और रैंडम फॉरेस्ट; जनवरी–मई तथा पिछले तीन मानसून के योग।'),
      (t('methods_eval'),t('ready'),
       'Training years 1874–1995, fixed reference 1871–1995, untouched holdout 1996–2016, no random future-year mixing.'
       if st.session_state.lang=='en' else 'प्रशिक्षण 1874–1995, संदर्भ 1871–1995, अलग परीक्षण 1996–2016; भविष्य के वर्ष प्रशिक्षण में नहीं।'),
      (t('methods_hybrid'),t('planned'),
       'ENSO/IOD and dated astronomical indicators require independent datasets and expert-checked calendar transformations.'
       if st.session_state.lang=='en' else 'ENSO/IOD तथा तिथि-सम्बद्ध खगोलीय संकेतकों के लिए स्वतंत्र डेटा और विशेषज्ञ-सत्यापित पंचांग रूपांतरण चाहिए।')]
    for n,(name,status,description) in enumerate(steps,1):
        a,b=st.columns([.16,.84],vertical_alignment='center')
        with a: st.metric('Step' if st.session_state.lang=='en' else 'चरण',n)
        with b:
            st.markdown(f'**{name}** · `{status}`')
            st.write(description)
        if n<len(steps):st.divider()
    st.write('')
    section(t('project_data'))
    st.markdown('**Homogeneous Indian Monthly Rainfall Data Sets (1871–2016)**')
    st.write(('Data supplied by the team; 2015–2016 use a different underlying collection basis according to the text-file header. Older separately provided archives are preserved, not automatically merged.'
        if st.session_state.lang=='en' else 'टीम द्वारा दिया गया डेटा; मूल फ़ाइल के अनुसार 2015–2016 में संग्रहण का आधार अलग है। अलग ऐतिहासिक संग्रह बिना जाँच के नहीं जोड़े गए।'))
    section(t('limitations'))
    notes=[
      ('Data only through 2016; no current or 2026 forecast is possible with this file.',
       'डेटा केवल 2016 तक है; इससे वर्तमान या 2026 का पूर्वानुमान नहीं हो सकता।'),
      ('Spatial values are aggregates; no official IMD gridded data or district boundaries are included.',
       'आँकड़े बड़े क्षेत्रों के औसत हैं; आधिकारिक ग्रिड या जिलों की सीमाएँ शामिल नहीं हैं।'),
      ('The All-India average overlaps the five regional aggregates; these are not six independent geographic bins.',
       'अखिल भारत अन्य पाँच क्षेत्रीय औसतों को समाहित करता है; ये छह स्वतंत्र भू-क्षेत्र नहीं हैं।'),
      ('Historical references are fixed at 1871–1995 and demo categories at ±10% anomaly.',
       'संदर्भ औसत 1871–1995 का है; ±10% वाली श्रेणियाँ केवल उदाहरण के लिए हैं।'),
      ('These ML models currently use rainfall history, not ENSO/IOD climate drivers or validated astronomical features.',
       'अभी मॉडल में सिर्फ पिछली वर्षा है; ENSO/IOD या सत्यापित खगोलीय संकेतक नहीं हैं।'),
      ('Traditional rules and original attributions are sourced from the provided CSV and are unverified.',
       'पारंपरिक नियम और स्रोत-उल्लेख दी गई CSV के अनुसार हैं; उनकी स्वतंत्र पुष्टि नहीं हुई है।'),
      ('Map marker positions are schematic; the India outline is from Natural Earth low-res reference data.',
       'मानचित्र के संकेतक स्थान उदाहरणार्थ हैं; भारत की बाहरी रेखा Natural Earth के कम रिज़ॉल्यूशन वाले संदर्भ डेटा से है।'),
    ]
    for en,hi in notes:st.markdown('• '+(hi if st.session_state.lang=='hi' else en))
    st.write('');section(t('classes'))
    st.info(t('classification_notice'))
    footnote()
