import streamlit as st
from core import evaluation as ev
from core.counter import accuracy
from . import theme, components
def render():
    theme.title("Pengujian Counting Accuracy", "Bandingkan jumlah sistem dengan hitungan manual (ground truth) pada waktu yang sama · target ≥ 80%")
    p = components.get_processor(); components.live_panel(show_video=False)
    st.caption("Tips: tekan **Jeda** di menu Pemrosesan Video agar frame diam, hitung anak di dalam kotak secara manual, lalu catat di sini.")
    with st.container():
        theme.mark(); st.markdown('<div class="card-h">Catat pengamatan</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.6, 1, 1.6])
        cond = c1.selectbox("Kondisi pengujian", ev.CONDITIONS); actual = c2.number_input("Jumlah aktual (manual)", 0, 500, 0); note = c3.text_input("Catatan (mis. menit video)")
        if st.button("Catat hasil (ambil jumlah sistem sekarang)", type="primary"):
            s = p.snapshot()
            if not s["available"]: st.error("Pemrosesan belum berjalan — jumlah sistem belum tersedia.")
            else: ev.add(cond, s["profile"] or "-", int(actual), int(s["count"]), note); st.success(f"Tercatat: aktual {actual}, sistem {s['count']}, akurasi {accuracy(s['count'], actual):.1f}%")
    sm = ev.summary(); a, b, c = st.columns(3)
    a.markdown(theme.card("Counting Accuracy rata-rata", f'{sm["accuracy"]}<small>%</small>' if sm["n"] else '<span class="na">Belum ada data</span>', "rata-rata seluruh pengamatan", icon="target", hero=True), unsafe_allow_html=True)
    b.markdown(theme.card("Jumlah pengamatan", sm["n"], "baris tersimpan di SQLite", icon="list"), unsafe_allow_html=True)
    c.markdown(theme.card("Target ≥ 80%", f'<span class="pill {"ok" if sm["passed"] else ("err" if sm["n"] else "off")}">{"Memenuhi" if sm["passed"] else ("Belum memenuhi" if sm["n"] else "Belum ada data")}</span>', "Counting accuracy minimal", True, icon="test", tone="ok" if sm["passed"] else ("err" if sm["n"] else "")), unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    with st.expander("Rumus yang digunakan"): st.markdown("Accuracy = (1 − |Aktual − Sistem| / Aktual) × 100%, minimum 0%.  \nJika Aktual = 0: 100% bila Sistem = 0, selain itu 0%.  \nCounting Accuracy akhir = rata-rata akurasi seluruh pengamatan.")
    rows = ev.rows()
    if rows:
        import pandas as pd, time
        df = pd.DataFrame([{"ID": r["id"], "Waktu": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r["ts"])), "Kondisi": r["cond"], "Profil ROI": r["profile"], "Aktual": r["truth"], "Sistem": r["system"], "Selisih": r["diff"], "Akurasi (%)": round(r["acc"], 1), "Catatan": r["note"]} for r in rows])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('<div class="sec-h">Ringkasan per kondisi</div>', unsafe_allow_html=True); st.dataframe(pd.DataFrame([{"Kondisi": k, "Pengamatan": n, "Rata-rata akurasi (%)": a} for k, (n, a) in sm["by_cond"].items()]), use_container_width=True, hide_index=True)
        d1, d2, d3 = st.columns([1, 1, 3]); d1.download_button("Unduh CSV", ev.to_csv(), "counting_accuracy.csv", "text/csv")
        did = d2.selectbox("Hapus ID", [r["id"] for r in rows], label_visibility="collapsed")
        if d3.button("Hapus baris terpilih"): ev.delete(did); st.rerun()
