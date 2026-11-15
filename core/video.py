import cv2, os
from . import config
def open_capture(source):
    t, v = source["type"], str(source["value"])
    if t == "webcam":
        i = int(v or 0)
        if os.name == "nt":                       # Windows: coba DirectShow dulu
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened(): return cap
            cap.release()
        return cv2.VideoCapture(i)
    if t == "mp4": return cv2.VideoCapture(v if os.path.isabs(v) else str(config.ROOT / v))
    return cv2.VideoCapture(v)                    # URL RTSP/CCTV
def source_error(source):
    t, v = source["type"], str(source["value"])
    if t == "mp4":
        p = v if os.path.isabs(v) else str(config.ROOT / v)
        if not os.path.exists(p): return f"File video tidak ditemukan: {p}"
        return "File video tidak dapat dibuka (format/codec tidak didukung)"
    if t == "webcam": return "Webcam tidak dapat dibuka. Tutup aplikasi lain yang memakai kamera, coba indeks 1, dan cek izin kamera Windows"
    return "Kamera/CCTV tidak dapat dibuka. Periksa URL dan koneksi jaringan"
def grab_frame(source, warmup=5):
    """Ambil satu frame dari sumber (untuk menggambar ROI). Return (frame_bgr|None, pesan_error|None)."""
    cap = open_capture(source)
    if not cap.isOpened(): return None, source_error(source)
    frame = None
    for _ in range(warmup if source["type"] != "mp4" else 1):
        ok, f = cap.read()
        if ok: frame = f
    cap.release()
    return (frame, None) if frame is not None else (None, "Tidak ada frame yang dapat dibaca dari sumber")
