import cv2, streamlit as st
from core import config, roi as roimod
from . import theme
def render():
    theme.title("Profil Kamera", "Profil ROI tersimpan untuk kamera/ruang kelas berbeda")
    profs = roimod.list_profiles(); act = config.load()["active_profile"]
    if not profs: st.info("Belum ada profil. Buat di menu Pengaturan ROI."); return
    for p in profs:
        with st.expander(f"{p['name']}" + ("  · AKTIF" if p["id"] == act else ""), expanded=p["id"] == act):
            c1, c2 = st.columns([1.3, 1]); img = cv2.imread(str(roimod.ref_path(p["id"])))
            if img is not None:
                H, W = img.shape[:2]; x1, y1, x2, y2 = roimod.to_pixels(p["roi"], W, H); cv2.rectangle(img, (x1, y1), (x2, y2), (184, 66, 112), max(2, W // 300))
                c1.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r = p["roi"]; c2.markdown(f"**Resolusi referensi:** {p['ref_width']}×{p['ref_height']}  \n**Sumber saat dibuat:** {p['source']['type']} · {p['source']['value']}  \n"
                                      f"**ROI (%):** ({r['x1']*100:.0f}, {r['y1']*100:.0f}) – ({r['x2']*100:.0f}, {r['y2']*100:.0f})  \n**Dibuat:** {p['created']}")
            if c2.button("Jadikan aktif", key=f"a{p['id']}"): config.update(active_profile=p["id"]); st.rerun()
            if c2.button("Hapus profil", key=f"d{p['id']}"): roimod.delete(p["id"]); st.rerun()
