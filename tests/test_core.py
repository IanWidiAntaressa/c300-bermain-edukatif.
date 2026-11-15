import os, sys, tempfile, pathlib, unittest
os.environ["C300_DATA"] = tempfile.mkdtemp()
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import numpy as np, cv2
from core.counter import ZoneCounter, accuracy
from core import roi, auth, evaluation as ev
R = {"x1": .3, "y1": .25, "x2": .7, "y2": .75}; W = H = 1000
def box(cx, fy): return (cx-30, fy-120, cx+30, fy)
class Counter(unittest.TestCase):
    def test_10_anak_4_dalam(self):
        d = [(i, box(400+i*30, 500)) for i in range(4)] + [(10+i, box(50+i*40, 900)) for i in range(6)]
        c, _, tot = ZoneCounter().update(d, R, W, H, 0.0); self.assertEqual((c, tot), (4, 10))
    def test_titik_kaki_bukan_overlap(self): self.assertEqual(ZoneCounter().update([(1, (400, 600, 460, 800))], R, W, H, 0)[0], 0)
    def test_tidak_ganda_tidak_akumulasi(self):
        zc = ZoneCounter()
        for t in range(50): c = zc.update([(1, box(500, 500))], R, W, H, t*.04)[0]
        self.assertEqual(c, 1)
    def test_masuk_keluar_dinamis(self):
        zc = ZoneCounter(); t = 0.0
        self.assertEqual(zc.update([(i, box(450+i*20, 500)) for i in range(3)], R, W, H, t)[0], 3)
        self.assertEqual(zc.update([(i, box(450+i*20, 500)) for i in range(4)], R, W, H, t+.1)[0], 4)          # 1 masuk
        self.assertEqual(zc.update([(0, box(450, 500)), (1, box(470, 500)), (2, box(60, 900)), (3, box(60, 900))], R, W, H, t+.2)[0], 2)   # 2 keluar
        self.assertEqual(zc.update([(0, box(450, 500)), (1, box(470, 500)), (2, box(60, 900)), (3, box(60, 900))], R, W, H, t+.3)[0], 2)
    def test_hilang_tidak_dihitung_selamanya(self):
        zc = ZoneCounter(1.0); zc.update([(1, box(500, 500))], R, W, H, 0)
        self.assertEqual(zc.update([], R, W, H, .5)[0], 1); self.assertEqual(zc.update([], R, W, H, 1.6)[0], 0)
    def test_tanpa_id(self): self.assertEqual(ZoneCounter().update([(None, box(500, 500))], R, W, H, 0)[0], 0)
    def test_accuracy(self):
        self.assertEqual(accuracy(4, 4), 100); self.assertEqual(accuracy(3, 4), 75); self.assertEqual(accuracy(0, 0), 100); self.assertEqual(accuracy(2, 0), 0); self.assertEqual(accuracy(9, 4), 0)
class Roi(unittest.TestCase):
    def test_validate(self):
        self.assertEqual(roi.validate({"x1": .7, "y1": .8, "x2": .2, "y2": .2}), {"x1": .2, "y1": .2, "x2": .7, "y2": .8})
        with self.assertRaises(ValueError): roi.validate({"x1": .5, "y1": .5, "x2": .51, "y2": .51})
    def test_proporsional(self): self.assertEqual(roi.to_pixels(R, 1920, 1080), (576, 270, 1344, 810)); self.assertEqual(roi.to_pixels(R, 640, 360), (192, 90, 448, 270))
    def test_profil_simpan_pakai_ulang_dan_kecocokan_scene(self):
        rng = np.random.RandomState(1); scene = cv2.GaussianBlur((rng.rand(360, 640, 3)*255).astype("uint8"), (0, 0), 1.5)
        for _ in range(60): cv2.rectangle(scene, tuple(rng.randint(0, 600, 2)), tuple(rng.randint(40, 640, 2)), tuple(int(v) for v in rng.randint(0, 255, 3)), 2)
        p = roi.save("Profil Test", R, scene, {"type": "mp4", "value": "x.mp4"}); self.assertEqual(roi.get(p["id"])["roi"], R)
        hi = cv2.resize(scene, (1280, 720)); noisy = np.clip(hi.astype(int) + rng.randint(-10, 10, hi.shape), 0, 255).astype("uint8")   # resolusi beda, scene sama
        self.assertTrue(roi.check_compat(p, noisy)[0])
        other = cv2.GaussianBlur((np.random.RandomState(9).rand(360, 640, 3)*255).astype("uint8"), (0, 0), 1.5)
        self.assertFalse(roi.check_compat(p, other)[0])                                      # scene beda -> peringatan
        self.assertFalse(roi.check_compat(p, cv2.resize(scene, (480, 480)))[0])              # rasio beda -> peringatan
        roi.delete(p["id"]); self.assertIsNone(roi.get(p["id"]))
class Auth(unittest.TestCase):
    def test_login(self):
        auth.ensure_default_admin(); self.assertTrue(auth.verify("admin", "admin123")); self.assertFalse(auth.verify("admin", "salah")); self.assertFalse(auth.verify("guest", ""))
        self.assertTrue(auth.change_password("admin", "admin123", "baru1234")); self.assertTrue(auth.verify("admin", "baru1234"))
class Eval(unittest.TestCase):
    def test_summary(self):
        ev.add("Anak berada di dalam ROI", "p", 4, 3); ev.add("Anak masuk ke ROI", "p", 10, 10)
        s = ev.summary(); self.assertEqual((s["n"], s["accuracy"], s["passed"]), (2, 87.5, True)); self.assertIn("87.5", ev.to_csv())
if __name__ == "__main__": unittest.main()
