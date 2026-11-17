"""Pemrosesan video: YOLOv8 (deteksi person) + ByteTrack (tracking) + penghitungan anak di dalam ROI. Berjalan di thread terpisah."""
import cv2, threading, time
from collections import deque
from . import config, roi as roimod
from .counter import ZoneCounter, foot_point
from .video import open_capture, source_error
GREEN, RED, PURPLE = (60, 180, 60), (60, 60, 230), (237, 58, 124)   # BGR (#7c3aed, aksen tema)
class Processor:
    def __init__(self):
        self.status, self.message = "stopped", ""; self.count, self.detected = 0, 0
        self.jpg = None; self.clean_jpg = None; self.raw = None; self.profile = None; self.source = None
        self.history = deque(maxlen=600); self._t = None; self._stop = threading.Event(); self._pause = threading.Event()
    @property
    def alive(self): return self._t is not None and self._t.is_alive()
    def snapshot(self):
        live = self.status in ("running", "paused")
        return {"status": self.status, "message": self.message, "available": live, "count": self.count if live else None,
                "detected": self.detected if live else None, "profile": self.profile["name"] if self.profile else None}
    def start(self, source, profile, force=False):
        if self.alive: return
        self._stop.clear(); self._pause.clear(); self.source, self.profile = source, profile; self.status, self.message = "starting", ""
        self.count = self.detected = 0; self.jpg = None; self.clean_jpg = None; self.history.clear()
        self._t = threading.Thread(target=self._run, args=(config.load(), source, profile, force), daemon=True); self._t.start()
    def stop(self):
        self._stop.set()
        if self._t: self._t.join(timeout=10)
        self.status, self.message, self.count, self.detected, self.jpg, self.clean_jpg, self.raw = "stopped", "", 0, 0, None, None, None
    def pause(self):
        if self.status == "running": self._pause.set(); self.status = "paused"
    def resume(self):
        if self.status == "paused": self._pause.clear(); self.status = "running"
    def _fail(self, st, msg): self.status, self.message = st, msg
    def _annotate(self, frame, roi, dets, inside, count):
        H, W = frame.shape[:2]; x1, y1, x2, y2 = roimod.to_pixels(roi, W, H)
        ov = frame.copy(); cv2.rectangle(ov, (x1, y1), (x2, y2), PURPLE, -1); frame = cv2.addWeighted(ov, 0.10, frame, 0.90, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), PURPLE, 3); cv2.putText(frame, "ZONA BERMAIN", (x1 + 6, y1 + 22), 0, 0.65, PURPLE, 2)
        for tid, box in dets:
            bx1, by1, bx2, by2 = map(int, box); fx, fy = map(int, foot_point(box)); col = GREEN if inside.get(tid, False) else RED
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), col, 2); cv2.circle(frame, (fx, fy), 5, col, -1)
            cv2.putText(frame, f"ID {tid}" if tid is not None else "ID ?", (bx1, max(14, by1 - 5)), 0, 0.55, col, 2)
        txt = f"Di dalam zona: {count}"; cv2.putText(frame, txt, (12, 32), 0, 0.9, (255, 255, 255), 4); cv2.putText(frame, txt, (12, 32), 0, 0.9, PURPLE, 2)
        return frame
    def _run(self, cfg, source, profile, force):
        try:
            from ultralytics import YOLO
            mp = config.MODELS / cfg["model"]; model = YOLO(str(mp) if mp.exists() else cfg["model"])   # unduh otomatis bila belum ada
        except Exception as e: return self._fail("error", f"Gagal memuat model YOLOv8: {e}")
        cap = open_capture(source)
        if not cap.isOpened(): return self._fail("error", source_error(source))
        ok, frame = cap.read()
        if not ok: cap.release(); return self._fail("error", "Tidak ada frame yang dapat dibaca dari sumber video")
        if not force:
            good, msg = roimod.check_compat(profile, frame, cfg["scene_match_min_inliers"], cfg["aspect_tolerance"])
            if not good: cap.release(); return self._fail("mismatch", msg)
        roi = profile["roi"]; counter = ZoneCounter(cfg["lost_grace_seconds"]); is_file = source["type"] == "mp4"
        fps = cap.get(cv2.CAP_PROP_FPS) or 25; self.status = "running"; self.message = ""; pending = frame
        while not self._stop.is_set():
            t0 = time.time()
            if self._pause.is_set(): time.sleep(0.1); continue
            if pending is None:
                ok, frame = cap.read()
                if not ok:
                    if is_file: self.status, self.message = "finished", "Video selesai diproses"; break
                    self.message = "Koneksi kamera terputus, mencoba menyambung kembali"; cap.release(); time.sleep(2); cap = open_capture(source); continue
            else: frame, pending = pending, None
            self.raw = frame; H, W = frame.shape[:2]
            try:
                r = model.track(frame, persist=True, tracker=cfg["tracker"], classes=[0], conf=cfg["conf"], imgsz=cfg["imgsz"], verbose=False)[0]
            except Exception as e: self._fail("error", f"Kesalahan deteksi: {e}"); break
            dets = []
            if r.boxes is not None and len(r.boxes):
                ids = r.boxes.id.int().cpu().tolist() if r.boxes.id is not None else [None] * len(r.boxes)
                dets = [(i, tuple(b)) for i, b in zip(ids, r.boxes.xyxy.cpu().numpy().tolist())]
            now = time.time(); count, inside, active = counter.update(dets, roi, W, H, now)
            self.count, self.detected = count, active; self.history.append((now, count))
            self.clean_jpg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()
            self.jpg = cv2.imencode(".jpg", self._annotate(frame.copy(), roi, dets, inside, count), [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()
            if is_file: time.sleep(max(0, 1 / fps - (time.time() - t0)))   # putar sesuai durasi asli
        cap.release()
