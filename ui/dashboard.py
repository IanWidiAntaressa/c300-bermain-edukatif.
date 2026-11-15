import streamlit as st
from core import auth
from . import theme, components
def render(role):
    theme.title("Dashboard", "Jumlah anak yang sedang berada di zona bermain secara real-time" + (" (tampilan Guest)" if role == "guest" else ""))
    components.live_panel(show_chart=(role == "admin"), clean_video=(role == "guest"))
    if role == "admin":
        with st.expander("Akun Admin · ubah password"):
            o = st.text_input("Password lama", type="password"); n = st.text_input("Password baru (min. 6 karakter)", type="password")
            if st.button("Ubah password"):
                st.success("Password diubah") if auth.change_password(st.session_state.auth["user"], o, n) else st.error("Password lama salah atau password baru terlalu pendek")
