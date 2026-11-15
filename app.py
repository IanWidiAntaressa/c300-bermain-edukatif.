import streamlit as st
st.set_page_config(page_title="Keterlibatan Bermain Edukatif", page_icon="🟣", layout="wide")
from core import auth
from ui import theme, login, dashboard, process, roi_page, profiles_page, testing_page
auth.ensure_default_admin()
if "auth" not in st.session_state: login.render(); st.stop()
theme.apply(); role = st.session_state.auth["role"]
PAGES = {"Dashboard": lambda: dashboard.render(role)}
if role == "admin": PAGES.update({"Pemrosesan Video": process.render, "Pengaturan ROI": roi_page.render, "Profil Kamera": profiles_page.render, "Pengujian Akurasi": testing_page.render})
with st.sidebar:
    st.markdown('<div class="brand">Bermain Edukatif</div><div class="sub">C300 · YOLOv8 + ByteTrack</div>', unsafe_allow_html=True)
    page = st.radio("Menu", list(PAGES), label_visibility="collapsed")
    st.markdown(f'<div class="sub" style="margin-top:18px">Masuk sebagai <b>{role.title()}</b></div>', unsafe_allow_html=True)
    if st.button("Keluar", use_container_width=True): del st.session_state["auth"]; st.rerun()
PAGES[page]()
