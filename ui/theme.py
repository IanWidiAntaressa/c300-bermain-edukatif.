import streamlit as st

# Tema disamakan dengan dashboard utama: netral hangat + aksen ungu, Lora (judul) + Plus Jakarta Sans (teks)
def _mask(path):
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' "
           f"stroke-linecap='round' stroke-linejoin='round'>{path}</svg>")
    return "url(\"data:image/svg+xml;utf8," + svg.replace("<", "%3C").replace(">", "%3E").replace("#", "%23") + "\")"

ICONS = {
    "home": "<path d='M3 11l9-8 9 8'/><path d='M5 10v10h14V10'/>",
    "video": "<path d='M23 7l-7 5 7 5V7z'/><rect x='1' y='5' width='15' height='14' rx='2'/>",
    "roi": "<rect x='4' y='4' width='16' height='16' rx='2' stroke-dasharray='3 3'/><circle cx='4' cy='4' r='1.5'/><circle cx='20' cy='20' r='1.5'/>",
    "profile": "<rect x='3' y='4' width='18' height='14' rx='2'/><path d='M3 14l5-4 4 3 3-2 6 4'/>",
    "test": "<path d='M9 11l3 3 8-8'/><path d='M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9'/>",
    "users": "<path d='M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><path d='M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75'/>",
    "cam": "<path d='M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z'/><circle cx='12' cy='13' r='4'/>",
    "pulse": "<path d='M22 12h-4l-3 9L9 3l-3 9H2'/>",
    "target": "<circle cx='12' cy='12' r='9'/><circle cx='12' cy='12' r='5'/><circle cx='12' cy='12' r='1'/>",
    "list": "<path d='M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01'/>",
}
def svg(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{ICONS.get(name, "")}</svg>'

_NAV = ["home", "video", "roi", "profile", "test"]
_NAV_CSS = "".join(
    f'section[data-testid="stSidebar"] div[role="radiogroup"]>label:nth-child({i + 1})::before,section[data-testid="stSidebar"] div[role="radiogroup"]>:nth-child({i + 1}) label::before{{-webkit-mask-image:{_mask(ICONS[n])};mask-image:{_mask(ICONS[n])}}}'
    for i, n in enumerate(_NAV))

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
:root{--bg:#faf9f7;--side:#f3f1ec;--panel:#ffffff;--ink:#1f1d1a;--mute:#5c574f;--line:#e5e0d8;--acc:#7c3aed;--acc-d:#6d28d9;--acc2:#c4a5fb;--soft:#efe8fd;--on-acc:#ffffff;
--ok:#15803d;--ok-soft:#dcf3e3;--warn:#b45309;--warn-soft:#fdecc8;--bad:#b42318;--bad-soft:#fde4e1;
--shadow:0 1px 2px rgba(31,29,26,.06),0 8px 24px rgba(31,29,26,.07);--r-card:20px;--r-inner:14px;--r-ctl:10px;--ctl:38px;--gap:16px;--pad:20px}

/* font & latar */
.stApp{background:var(--bg);color:var(--ink)}
.stApp,.stApp :is(p,li,label,input,textarea,button,td,th,h1,h2,h3,h4,h5,small,div,span):not([data-testid*="Icon"]):not([class*="material"]):not(.katex *){font-family:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header[data-testid="stHeader"]{background:transparent}
.block-container,[data-testid="stMainBlockContainer"]{max-width:1120px;padding-top:32px;padding-bottom:56px}
.stApp h1,.stApp h2,.stApp h3{color:var(--ink)}
.stMarkdown strong{font-weight:650}
[data-testid="stCaptionContainer"]{color:var(--mute)}

/* sidebar */
section[data-testid="stSidebar"]{background:var(--side);border-right:1px solid var(--line)}
section[data-testid="stSidebar"]>div{background:var(--side)}
.brand{display:flex;align-items:center;gap:12px;padding:4px 4px 20px;font-weight:700;font-size:16px;color:var(--ink);line-height:1.25}
.brand small{display:block;font-weight:400;font-size:12px;color:var(--mute)}
.logo{width:34px;height:34px;border-radius:11px;background:var(--acc);color:var(--on-acc);display:grid;place-items:center;flex:none}
.logo .ic{width:18px;height:18px}
section[data-testid="stSidebar"] div[role="radiogroup"]{gap:4px;flex-direction:column;width:100%}
section[data-testid="stSidebar"] div[role="radiogroup"] label{display:flex;align-items:center;gap:12px;width:100%;height:var(--ctl);padding:0 12px;margin:0;border-radius:var(--r-ctl);color:var(--mute);font-weight:500;cursor:pointer;transition:background .15s}
section[data-testid="stSidebar"] div[role="radiogroup"]>div{width:100%}
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]>div:first-child,
section[data-testid="stSidebar"] div[role="radiogroup"] label>div>div:first-child:not([data-testid="stMarkdownContainer"]){display:none}
section[data-testid="stSidebar"] div[role="radiogroup"] label::before{content:"";width:18px;height:18px;flex:none;background:currentColor;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:contain;mask-size:contain}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{color:inherit;font-weight:inherit;font-size:15px}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:color-mix(in srgb,var(--acc) 7%,transparent)}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:var(--soft);color:var(--acc);font-weight:650}
.sfoot{margin-top:24px;padding:16px 4px 12px;border-top:1px solid var(--line);font-size:13px;color:var(--mute)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--ok);margin-right:8px}

/* judul halaman */
.page-title{font-family:Lora,Georgia,serif!important;font-weight:500;font-size:clamp(26px,4vw,34px);line-height:1.2;color:var(--ink);margin:0}
.page-sub{color:var(--mute);margin:4px 0 24px;font-size:15px}

/* kartu statistik */
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-card);padding:var(--pad);box-shadow:var(--shadow);height:100%;min-width:0;display:flex;flex-direction:column;align-items:flex-start}
.card.hero{background:linear-gradient(165deg,var(--soft) 0%,var(--panel) 62%)}
.st-ic{width:34px;height:34px;flex:none;border-radius:11px;display:grid;place-items:center;background:var(--soft);color:var(--acc);margin-bottom:12px}
.st-ic.ok{background:var(--ok-soft);color:var(--ok)}.st-ic.warn{background:var(--warn-soft);color:var(--warn)}.st-ic.err{background:var(--bad-soft);color:var(--bad)}
.ic{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}
.card .lbl{color:var(--mute);font-size:13px;font-weight:500}
.card .val{font-family:Lora,Georgia,serif!important;font-weight:500;font-size:clamp(34px,5vw,46px);line-height:1.1;color:var(--ink);margin-top:6px;font-variant-numeric:tabular-nums}
.card .val small{font-family:"Plus Jakarta Sans",system-ui,sans-serif!important;font-size:15px;color:var(--mute);font-weight:500;margin-left:4px}
.card .val.sm{font-family:"Plus Jakarta Sans",system-ui,sans-serif!important;font-size:16px;margin-top:8px;font-weight:600}
.card .hint{color:var(--mute);font-size:13px;margin-top:6px;line-height:1.4}

[data-testid="stColumn"]:has(.card) :has(.card){height:100%}
.card .val .na{font-family:"Plus Jakarta Sans",system-ui,sans-serif;font-size:20px;font-weight:600;color:var(--mute)}

/* chip status */
.pill{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:999px;font-size:14px;font-weight:600;background:var(--soft);color:var(--acc)}
.pill::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.pill.ok{background:var(--ok-soft);color:var(--ok)}.pill.warn{background:var(--warn-soft);color:var(--warn)}
.pill.err{background:var(--bad-soft);color:var(--bad)}.pill.off{background:var(--side);color:var(--mute)}

/* video */
.vid{position:relative;background:#0f0e0c;border-radius:var(--r-card);overflow:hidden;box-shadow:var(--shadow)}
.vid img{width:100%;display:block}
.vid .empty{min-height:340px;display:grid;place-content:center;justify-items:center;gap:12px;text-align:center;color:#e9e4da;padding:20px;font-size:14px}
.vid .empty .logo{width:52px;height:52px;border-radius:16px}
.vid .empty .logo .ic{width:24px;height:24px}
.sec-h{font-size:16px;font-weight:650;margin:20px 0 10px;color:var(--ink)}

/* kontainer kartu: st.container() yang berisi theme.mark() */
[data-testid="stVerticalBlock"]:has(> div .card-mark):not(:has(> div [data-testid="stVerticalBlock"] .card-mark)){background:var(--panel);border:1px solid var(--line);border-radius:var(--r-card);padding:var(--pad);box-shadow:var(--shadow)}
[data-testid="stElementContainer"]:has(.card-mark),.element-container:has(.card-mark){display:none}
.card-h{font-size:16px;font-weight:650;color:var(--ink);margin:0}

/* tombol: tinggi seragam */
.stButton>button,.stDownloadButton>button,button[data-testid^="stBaseButton"]{min-height:var(--ctl);border-radius:var(--r-ctl);border:1px solid var(--line);background:var(--panel);color:var(--ink);font-weight:600;box-shadow:none;transition:border-color .15s,background .15s}
.stButton>button:hover,.stDownloadButton>button:hover,button[data-testid="stBaseButton-secondary"]:hover{border-color:var(--acc);color:var(--acc);background:var(--panel)}
.stButton>button[kind="primary"],button[data-testid="stBaseButton-primary"]{background:var(--acc);border-color:var(--acc);color:var(--on-acc)}
.stButton>button[kind="primary"]:hover,button[data-testid="stBaseButton-primary"]:hover{background:var(--acc-d);border-color:var(--acc-d);color:var(--on-acc)}
.stButton>button:disabled{opacity:.5}
.stButton>button p,.stDownloadButton>button p{font-weight:600}

/* input */
[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"],.stSelectbox [role="group"],.stSelectbox [data-baseweb="select"]>div,
div[data-baseweb="input"],div[data-baseweb="textarea"]{border:1px solid var(--line);border-radius:var(--r-ctl)!important;border-color:var(--line)!important;background:var(--panel)!important}
div[data-baseweb="input"] input,div[data-baseweb="base-input"],div[data-baseweb="select"] div{background:transparent}
[data-testid="stTextInputRootElement"]:focus-within,[data-testid="stNumberInputContainer"]:focus-within,.stSelectbox [role="group"]:focus-within,
div[data-baseweb="input"]:focus-within,div[data-baseweb="select"]>div:focus-within{border-color:var(--acc)!important}
[data-testid="stNumberInput"] button,[data-testid="stTextInputRootElement"] input,[data-testid="stNumberInputContainer"] input{background:var(--panel)!important;border-color:var(--line)!important;color:var(--mute)}
[data-testid="stWidgetLabel"] p{font-size:13.5px;font-weight:500;color:var(--ink)}
[data-testid="stFileUploaderDropzone"]{background:var(--bg);border:1px dashed var(--line);border-radius:var(--r-inner)}
.stRadio [role="radiogroup"] label p{font-size:14px}

/* tab, expander, alert, tabel */
.stTabs [data-baseweb="tab-list"]{gap:4px;border-bottom:1px solid var(--line)}
.stTabs [data-baseweb="tab"]{height:38px;padding:0 14px;border-radius:var(--r-ctl) var(--r-ctl) 0 0;color:var(--mute);font-weight:500}
.stTabs [aria-selected="true"]{color:var(--acc)!important;font-weight:650}
.stTabs [data-baseweb="tab-highlight"]{background:var(--acc)}
.stTabs [data-baseweb="tab-border"]{display:none}
[data-testid="stExpander"] details{border:1px solid var(--line);border-radius:var(--r-inner);background:var(--panel);box-shadow:var(--shadow)}
[data-testid="stExpander"] summary{font-weight:600}
[data-testid="stExpander"] summary:hover{color:var(--acc)}
[data-testid="stAlert"]>div,div[role="alert"]{border-radius:var(--r-inner)}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:var(--r-inner);overflow:hidden}
[data-testid="stImage"] img,iframe{border-radius:var(--r-inner)}
[data-testid="stVegaLiteChart"],[data-testid="stArrowVegaLiteChart"]{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-card);padding:12px;box-shadow:var(--shadow)}

/* login */
.login-head{display:flex;flex-direction:column;align-items:center;text-align:center;gap:10px;margin-bottom:6px}
.login-head .logo{width:52px;height:52px;border-radius:16px}.login-head .logo .ic{width:24px;height:24px}
.login-head .page-title{font-size:clamp(24px,3vw,30px)}.login-head .page-sub{margin:0 0 8px}
""" + _NAV_CSS + "</style>"


def apply(): st.markdown(CSS, unsafe_allow_html=True)


def title(t, sub=""):
    st.markdown(f'<div class="page-title">{t}</div><div class="page-sub">{sub}</div>', unsafe_allow_html=True)


def mark():
    """Panggil di awal `with st.container():` agar kontainer tampil sebagai kartu."""
    st.markdown('<div class="card-mark"></div>', unsafe_allow_html=True)


def card(label, value, hint="", small=False, icon=None, tone="", hero=False):
    ic = f'<div class="st-ic {tone}">{svg(icon)}</div>' if icon else ""
    return (f'<div class="card{" hero" if hero else ""}">{ic}<div class="lbl">{label}</div>'
            f'<div class="val{" sm" if small else ""}">{value}</div><div class="hint">{hint}</div></div>')
