import streamlit as st
from core import config, roi as roimod
from . import theme, components
def render():
    theme.title("Pemrosesan Video", "Pilih sumber video dan profil ROI, lalu mulai deteksi")
    p = components.get_processor(); cfg = config.load(); src = cfg["source"]
    with st.container():
        theme.mark(); st.markdown('<div class="card-h">Sumber video</div>', unsafe_allow_html=True)
        labels = {"mp4": "File video MP4", "webcam": "Webcam laptop", "rtsp": "Kamera/CCTV (URL)"}
        t = st.radio("Jenis sumber", list(labels), format_func=labels.get, index=list(labels).index(src["type"]), horizontal=True)
        val = src["value"] if src["type"] == t else ""
        if t == "mp4":
            up = st.file_uploader("Unggah MP4 dari komputer", type=["mp4"])
            if up is not None:
                d = config.VIDEOS / up.name.replace("/", "_").replace("\\", "_")
                if not d.exists() or d.stat().st_size != up.size: d.write_bytes(up.getbuffer())
                val = f"videos/{d.name}"
            files = sorted(f.name for f in config.VIDEOS.glob("*.mp4"))
            if files:
                cur = val.split("/")[-1] if val else files[0]; val = "videos/" + st.selectbox("Atau pilih file di folder videos/", files, index=files.index(cur) if cur in files else 0)
            else: st.info("Belum ada MP4 di folder videos/. Unggah file di atas.")
        elif t == "webcam": val = str(st.number_input("Indeks webcam (0 = kamera utama)", 0, 10, int(val) if str(val).isdigit() else 0))
        else: val = st.text_input("URL kamera/CCTV", val, placeholder="rtsp://user:pass@192.168.1.x:554/stream1")
        profs = roimod.list_profiles()
        if profs:
            ids = [x["id"] for x in profs]; cur = cfg["active_profile"] if cfg["active_profile"] in ids else ids[0]
            pid = st.selectbox("Profil ROI", ids, index=ids.index(cur), format_func=lambda i: next(x["name"] for x in profs if x["id"] == i))
        else: pid = None; st.warning("Belum ada profil ROI. Buat dulu di menu Pengaturan ROI.")
    alive = p.alive; s = p.snapshot()
    c1, c2, c3, _ = st.columns([1, 1, 1, 2])
    if c1.button("Mulai", type="primary", use_container_width=True, disabled=alive or not pid or not val):
        config.update(source={"type": t, "value": val}, active_profile=pid); p.start({"type": t, "value": val}, roimod.get(pid)); st.rerun()
    if s["status"] == "paused":
        if c2.button("Lanjutkan", use_container_width=True): p.resume(); st.rerun()
    elif c2.button("Jeda", use_container_width=True, disabled=s["status"] != "running"): p.pause(); st.rerun()
    if c3.button("Berhenti", use_container_width=True, disabled=not alive and s["status"] in ("stopped",)): p.stop(); st.rerun()
    if s["status"] == "mismatch":
        st.warning(f"⚠ {s['message']} ROI tersimpan mungkin tidak sesuai dengan video ini. Pilih profil yang benar, atau buat ROI baru di menu Pengaturan ROI.")
        if st.button("Tetap gunakan profil ini"): p.start(p.source, p.profile, force=True); st.rerun()
    if s["status"] == "error": st.error(s["message"])
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    components.live_panel()
