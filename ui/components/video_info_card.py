#ui\components\video_info_card.py
import streamlit as st

def render_video_info_card(info: dict):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(info['thumbnail'], width="stretch")
    
    with col2:
        st.subheader(info['title'])
        st.markdown(f"**Canal:** {info['uploader']}")
        st.markdown(f"**Duración:** {info['duration']} segundos")
        st.markdown(f"**Categoría:** {info['categories']}")
        
        with st.expander("Ver formatos disponibles"):
            st.markdown("**Video:**")
            for quality in info["video_formats"]:
                st.markdown(f"- {quality}")
            
            st.markdown("**Audio:**")
            for quality in info["audio_formats"]:
                st.markdown(f"- {quality}")