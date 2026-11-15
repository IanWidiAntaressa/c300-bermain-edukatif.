import json, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = pathlib.Path(os.environ.get("C300_DATA", ROOT / "data"))
VIDEOS, MODELS, PROFILE_IMG = ROOT / "videos", ROOT / "models", DATA / "profiles"
for _d in (DATA, VIDEOS, MODELS, PROFILE_IMG): _d.mkdir(parents=True, exist_ok=True)
CFG = DATA / "config.json"
DEFAULTS = {"model": "yolov8n.pt", "conf": 0.35, "imgsz": 640, "tracker": "bytetrack.yaml", "lost_grace_seconds": 1.0,
            "scene_match_min_inliers": 12, "aspect_tolerance": 0.08, "source": {"type": "mp4", "value": "videos/kelas.mp4"}, "active_profile": None}
def load():
    c = dict(DEFAULTS)
    try: c.update(json.loads(CFG.read_text(encoding="utf-8")))
    except Exception: pass
    return c
def save(c): CFG.write_text(json.dumps(c, indent=2, ensure_ascii=False), encoding="utf-8")
def update(**kw): c = load(); c.update(kw); save(c); return c
