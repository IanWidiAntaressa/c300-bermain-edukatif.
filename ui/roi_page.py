import cv2, streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates as sic
from core import config, roi as roimod
from core.video import grab_frame
from . import theme, components
IMG_W = 760; K = ("s_x1", "s_y1", "s_x2", "s_y2")
def _set_sliders(r):
    for k, v in zip(K, ("x1", "y1", "x2", "y2")): st.session_state[k] = round(r[v] * 100, 1)
def _load_profile():
    sel = st.session_state.get("roi_sel"); st.session_state.roi_clicks = []
    if sel and sel != "(baru)":
        p = roimod.get(sel)
        if p: _set_sliders(p["roi"]); st.session_state.roi_name = p["name"]; st.session_state.roi_frame = cv2.imread(str(roimod.ref_path(sel)))
    else: _set_sliders(roimod.DEFAULT_ROI); st.session_state.roi_name = ""
def render():
    theme.title("Pengaturan ROI", "Gambar SATU kotak zona bermain di tengah kelas. Cukup sekali per kamera, lalu simpan sebagai profil.")
    ss = st.session_state; ss.setdefault("roi_clicks", []); ss.setdefault("roi_frame", None)
    if "roi_sel_next" in ss: ss.roi_sel = ss.pop("roi_sel_next")      # ubah pilihan profil SEBELUM widget dibuat
    if "roi_msg" in ss: st.success(ss.pop("roi_msg"))
    if "s_x1" not in ss: _set_sliders(roimod.DEFAULT_ROI)
    profs = roimod.list_profiles(); opts = ["(baru)"] + [p["id"] for p in profs]
    names = {p["id"]: p["name"] for p in profs}; names["(baru)"] = "+ Profil baru"
    st.selectbox("Profil ROI yang diedit (Ubah Zona)", opts, key="roi_sel", format_func=names.get, on_change=_load_profile)
    p = components.get_processor(); cfg = config.load()
    b1, b2, _ = st.columns([1.2, 1.2, 3])
    if b1.button("Ambil frame dari sumber aktif", use_container_width=True):
        f = p.raw.copy() if p.raw is not None and p.alive else None; err = None
        if f is None: f, err = grab_frame(cfg["source"])
        if f is None: st.error(err)
        else: ss.roi_frame = f; ss.roi_clicks = []
    if b2.button("Reset Zona", use_container_width=True): _set_sliders(roimod.DEFAULT_ROI); ss.roi_clicks = []
    frame = ss.roi_frame
    if frame is None: st.info("Ambil frame dari sumber (video/webcam yang dipilih di menu Pemrosesan Video) atau pilih profil tersimpan untuk mengubah zonanya."); return
    left, right = st.columns([2.2, 1])
    with left:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB); H, W = rgb.shape[:2]
        r = {"x1": ss.s_x1 / 100, "y1": ss.s_y1 / 100, "x2": ss.s_x2 / 100, "y2": ss.s_y2 / 100}
        try: rv = roimod.validate(r) if r["x1"] < r["x2"] and r["y1"] < r["y2"] else None
        except ValueError: rv = None
        if rv:
            x1, y1, x2, y2 = roimod.to_pixels(rv, W, H); ov = rgb.copy(); cv2.rectangle(ov, (x1, y1), (x2, y2), (124, 58, 237), -1)
            rgb = cv2.addWeighted(ov, .15, rgb, .85, 0); cv2.rectangle(rgb, (x1, y1), (x2, y2), (124, 58, 237), max(2, W // 300))
        for (cx, cy) in ss.roi_clicks: cv2.circle(rgb, (int(cx * W), int(cy * H)), max(5, W // 150), (255, 255, 255), -1)
        st.caption("Klik sudut pertama, lalu klik sudut berlawanan pada gambar. Sesuaikan posisi/ukuran dengan slider di kanan.")
        res = sic(Image.fromarray(rgb), key="roi_img", width=IMG_W)
        if res and res.get("width"):
            sig = (res["x"], res["y"], res.get("unix_time"))
            if sig != ss.get("roi_last"):
                ss.roi_last = sig; ss.roi_clicks.append((res["x"] / res["width"], res["y"] / res["height"]))
                if len(ss.roi_clicks) >= 2:
                    (ax, ay), (bx, by) = ss.roi_clicks[-2:]; _set_sliders({"x1": min(ax, bx), "y1": min(ay, by), "x2": max(ax, bx), "y2": max(ay, by)}); ss.roi_clicks = []
                st.rerun()
    with right:
        st.markdown("**Posisi & ukuran (%)**")
        st.slider("Kiri (x1)", 0.0, 100.0, key="s_x1", step=0.5); st.slider("Atas (y1)", 0.0, 100.0, key="s_y1", step=0.5)
        st.slider("Kanan (x2)", 0.0, 100.0, key="s_x2", step=0.5); st.slider("Bawah (y2)", 0.0, 100.0, key="s_y2", step=0.5)
        name = st.text_input("Nama profil", key="roi_name", placeholder="mis. Profil Kamera Kelas 1")
        if st.button("Simpan Zona", type="primary", use_container_width=True):
            if rv is None: st.error("Zona tidak valid (kiri harus < kanan, atas < bawah, ukuran cukup besar)")
            elif not name.strip(): st.error("Isi nama profil")
            else:
                pid = ss.roi_sel if ss.roi_sel != "(baru)" else None
                saved = roimod.save(name, rv, frame, cfg["source"], pid); config.update(active_profile=saved["id"])
                ss.roi_sel_next = saved["id"]; ss.roi_msg = f"Zona disimpan sebagai profil '{saved['name']}' ({saved['ref_width']}×{saved['ref_height']}) dan dijadikan aktif."; st.rerun()
