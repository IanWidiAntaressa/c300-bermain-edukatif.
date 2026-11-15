"""Profil ROI permanen (JSON). Koordinat disimpan ternormalisasi 0-1 sehingga otomatis proporsional di resolusi apa pun.
Kecocokan sudut pandang dicek dengan pencocokan fitur ORB + RANSAC terhadap frame referensi profil."""
import json, time, uuid, cv2
from . import config
F = config.DATA / "roi_profiles.json"
DEFAULT_ROI = {"x1": 0.30, "y1": 0.25, "x2": 0.70, "y2": 0.75}
def validate(roi):
    r = {k: max(0.0, min(1.0, float(roi[k]))) for k in ("x1", "y1", "x2", "y2")}
    x1, x2 = sorted((r["x1"], r["x2"])); y1, y2 = sorted((r["y1"], r["y2"]))
    if x2 - x1 < 0.03 or y2 - y1 < 0.03: raise ValueError("Zona terlalu kecil")
    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
def _read():
    try: return json.loads(F.read_text(encoding="utf-8"))
    except Exception: return []
def list_profiles(): return _read()
def get(pid): return next((p for p in _read() if p["id"] == pid), None)
def ref_path(pid): return config.PROFILE_IMG / f"{pid}.jpg"
def save(name, roi, frame_bgr, source, pid=None):
    if not name.strip(): raise ValueError("Nama profil wajib diisi")
    roi = validate(roi); ps = _read(); pid = pid or uuid.uuid4().hex[:8]
    h, w = frame_bgr.shape[:2]
    cv2.imwrite(str(ref_path(pid)), frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
    p = {"id": pid, "name": name.strip(), "roi": roi, "ref_width": w, "ref_height": h, "source": source, "created": time.strftime("%Y-%m-%d %H:%M:%S")}
    ps = [x for x in ps if x["id"] != pid] + [p]; F.write_text(json.dumps(ps, indent=2, ensure_ascii=False), encoding="utf-8"); return p
def delete(pid):
    F.write_text(json.dumps([p for p in _read() if p["id"] != pid], indent=2, ensure_ascii=False), encoding="utf-8")
    try: ref_path(pid).unlink()
    except FileNotFoundError: pass
def to_pixels(roi, W, H): return (int(roi["x1"]*W), int(roi["y1"]*H), int(roi["x2"]*W), int(roi["y2"]*H))
def scene_match(ref_bgr, cur_bgr, min_inliers=12):
    """Return (cocok:bool, jumlah_inlier:int)."""
    def prep(im):
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); h, w = g.shape; return cv2.resize(g, (640, max(1, int(h*640/w))))
    orb = cv2.ORB_create(1500); k1, d1 = orb.detectAndCompute(prep(ref_bgr), None); k2, d2 = orb.detectAndCompute(prep(cur_bgr), None)
    if d1 is None or d2 is None or len(k1) < 10 or len(k2) < 10: return False, 0
    knn = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1, d2, k=2)
    good = [p[0] for p in knn if len(p) == 2 and p[0].distance < 0.75 * p[1].distance]
    if len(good) < min_inliers: return False, len(good)
    import numpy as np
    src = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2); dst = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0); inl = int(mask.sum()) if mask is not None else 0
    return inl >= min_inliers, inl
def check_compat(profile, cur_bgr, min_inliers=12, aspect_tol=0.08):
    """Return (ok, pesan). Peringatan jika rasio gambar atau pemandangan tidak cocok dengan profil."""
    h, w = cur_bgr.shape[:2]; ra, rb = profile["ref_width"]/profile["ref_height"], w/h
    if abs(ra-rb)/ra > aspect_tol: return False, f"Rasio gambar berbeda (profil {profile['ref_width']}x{profile['ref_height']}, video {w}x{h})."
    ref = cv2.imread(str(ref_path(profile["id"])))
    if ref is None: return True, "Frame referensi profil tidak ditemukan; kecocokan tidak dapat diperiksa."
    ok, n = scene_match(ref, cur_bgr, min_inliers)
    return (True, f"Sudut pandang cocok ({n} titik fitur sama).") if ok else (False, f"Sudut pandang/tata letak tampak berbeda dari profil ({n} titik fitur cocok, minimal {min_inliers}).")
