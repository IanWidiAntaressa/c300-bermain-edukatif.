import base64, streamlit as st
from core.processor import Processor
from . import theme
@st.cache_resource
def get_processor(): return Processor()
STATUS = {"stopped": ("Berhenti", "off"), "starting": ("Memulai…", ""), "running": ("Berjalan", "ok"), "paused": ("Dijeda", "warn"),
          "mismatch": ("ROI perlu ditinjau", "err"), "error": ("Error", "err"), "finished": ("Video selesai", "off")}
def video_html(jpg):
    if not jpg: return f'<div class="vid"><div class="empty"><div class="logo">{theme.svg("video")}</div>Video belum aktif. Mulai pemrosesan pada menu Pemrosesan Video.</div></div>'
    return f'<div class="vid"><img src="data:image/jpeg;base64,{base64.b64encode(jpg).decode()}"></div>'
@st.fragment(run_every=0.5)
def live_panel(show_chart=False, show_video=True, clean_video=False):
    p = get_processor(); s = p.snapshot(); label, cls = STATUS.get(s["status"], (s["status"], ""))
    c1, c2, c3 = st.columns([1.3, 1, 1])
    c1.markdown(theme.card("Anak di dalam zona bermain", f'{s["count"]}<small>anak</small>' if s["available"] else '<span class="na">Belum tersedia</span>', "Jumlah saat ini, bukan akumulasi", icon="users", hero=True), unsafe_allow_html=True)
    cam = "Aktif" if s["available"] else "Tidak aktif"
    c2.markdown(theme.card("Status kamera", f'<span class="pill {"ok" if s["available"] else "off"}">{cam}</span>', f'Profil ROI: {s["profile"] or "-"}', True, icon="cam", tone="ok" if s["available"] else ""), unsafe_allow_html=True)
    c3.markdown(theme.card("Status sistem", f'<span class="pill {cls}">{label}</span>', (s["message"] or (f'ID terlacak aktif: {s["detected"]}' if s["available"] else ""))[:90], True, icon="pulse", tone={"err": "err", "warn": "warn", "ok": "ok"}.get(cls, "")), unsafe_allow_html=True)
    if show_video:
        displayed_frame = p.clean_jpg if clean_video else p.jpg
        st.markdown("<div style='height:16px'></div>" + video_html(displayed_frame), unsafe_allow_html=True)
    if show_chart and len(p.history) > 2:
        import pandas as pd
        h = list(p.history)[-300:]; df = pd.DataFrame({"Anak di zona": [c for _, c in h]}, index=[pd.to_datetime(t, unit="s") for t, _ in h])
        st.markdown('<div class="sec-h">Grafik jumlah anak di zona (±5 menit terakhir)</div>', unsafe_allow_html=True); st.line_chart(df, color="#7c3aed", height=200)
