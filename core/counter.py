"""Penghitungan murni (tanpa YOLO/OpenCV). Acuan posisi = titik bottom-center bounding box.
Yang ditampilkan = jumlah anak SAAT INI di dalam ROI (bukan akumulasi). Satu tracking ID dihitung satu kali."""
def foot_point(box):
    x1, y1, x2, y2 = box; return ((x1 + x2) / 2, y2)
def in_roi(pt, roi, W, H):
    x, y = pt; return roi["x1"]*W <= x <= roi["x2"]*W and roi["y1"]*H <= y <= roi["y2"]*H
class ZoneCounter:
    def __init__(self, grace=1.0, purge=30.0): self.grace, self.purge, self.tracks = grace, purge, {}
    def reset(self): self.tracks = {}
    def update(self, dets, roi, W, H, now):
        """dets: [(track_id|None, (x1,y1,x2,y2))] -> (jumlah_di_ROI, {id: di_dalam?}, jumlah_ID_aktif).
        Track yang hilang > grace detik tidak dihitung lagi (tidak dihitung tanpa batas waktu)."""
        seen = {}
        for tid, box in dets:
            if tid is None: continue                                  # belum punya ID -> tidak dihitung (hindari ganda)
            ins = in_roi(foot_point(box), roi, W, H); seen[tid] = ins; self.tracks[tid] = {"seen": now, "inside": ins}
        for t in [t for t, v in self.tracks.items() if now - v["seen"] > self.purge]: del self.tracks[t]
        active = {t: v["inside"] for t, v in self.tracks.items() if now - v["seen"] <= self.grace}
        return sum(1 for v in active.values() if v), seen, len(active)
def accuracy(system, actual):
    """Accuracy = (1 - |Aktual - Sistem| / Aktual) x 100%, minimum 0. Aktual = 0: 100% jika Sistem = 0, selain itu 0%."""
    if actual == 0: return 100.0 if system == 0 else 0.0
    return max(0.0, (1 - abs(actual - system) / actual) * 100.0)
