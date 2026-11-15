import csv, io, time
from .db import conn
from .counter import accuracy
CONDITIONS = ["Anak berada di dalam ROI", "Anak berada di luar ROI", "Anak masuk ke ROI", "Anak keluar dari ROI",
              "Beberapa anak bergerak bersamaan", "Anak berdekatan / tertutup sebagian", "Anak tidak terlihat kamera", "Lainnya"]
TARGET = 80.0
def add(cond, profile, actual, system, note=""):
    with conn() as c:
        c.execute("INSERT INTO eval(ts,cond,profile,truth,system,diff,acc,note) VALUES(?,?,?,?,?,?,?,?)",
                  (int(time.time()), cond, profile, actual, system, system - actual, accuracy(system, actual), note))
def rows():
    with conn() as c: return [dict(r) for r in c.execute("SELECT * FROM eval ORDER BY id")]
def delete(i):
    with conn() as c: c.execute("DELETE FROM eval WHERE id=?", (i,))
def summary():
    r = rows(); n = len(r)
    if not n: return {"n": 0, "accuracy": None, "passed": None, "by_cond": {}}
    by = {}
    for x in r: by.setdefault(x["cond"], []).append(x["acc"])
    a = sum(x["acc"] for x in r) / n
    return {"n": n, "accuracy": round(a, 2), "passed": a >= TARGET, "by_cond": {k: (len(v), round(sum(v)/len(v), 2)) for k, v in by.items()}}
def to_csv():
    o = io.StringIO(); w = csv.writer(o); w.writerow(["waktu", "kondisi", "profil_roi", "aktual", "sistem", "selisih", "akurasi_%", "catatan"])
    for r in rows(): w.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r["ts"])), r["cond"], r["profile"], r["truth"], r["system"], r["diff"], round(r["acc"], 2), r["note"]])
    s = summary(); w.writerow([]); w.writerow(["Counting Accuracy rata-rata", s["accuracy"], "target 80%", "MEMENUHI" if s["passed"] else "BELUM"]); return o.getvalue()
