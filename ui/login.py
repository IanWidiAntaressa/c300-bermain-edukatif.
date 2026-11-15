import streamlit as st
from core import auth
from . import theme
def render():
    theme.apply(); _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        theme.title("Keterlibatan Bermain Edukatif", "Kalkulasi jumlah anak di zona bermain · YOLOv8 + ByteTrack")
        tab_a, tab_g = st.tabs(["Admin", "Guest"])
        with tab_a:
            u = st.text_input("Username", key="lu"); p = st.text_input("Password", type="password", key="lp")
            if st.button("Masuk sebagai Admin", type="primary", use_container_width=True):
                if auth.verify(u, p): st.session_state.auth = {"role": "admin", "user": u}; st.rerun()
                else: st.error("Username atau password salah")
        with tab_g:
            st.write("Guest hanya dapat melihat video hasil pemrosesan, jumlah anak di zona, dan status. Tidak ada akses pengaturan.")
            if st.button("Masuk sebagai Guest", use_container_width=True): st.session_state.auth = {"role": "guest", "user": "guest"}; st.rerun()
