import streamlit as st
CSS = """<style>
.stApp{background:#F5F5F7;color:#292633}
header[data-testid="stHeader"]{background:transparent}
section[data-testid="stSidebar"]{background:#FFFFFF;border-right:1px solid #E5E5E9}
section[data-testid="stSidebar"] .brand{font-weight:700;font-size:18px;color:#593193;margin:4px 0 2px}
section[data-testid="stSidebar"] .sub{color:#85818E;font-size:12px;margin-bottom:14px}
h1,h2,h3{color:#292633}
.page-title{font-size:26px;font-weight:700;color:#292633;margin:0}.page-sub{color:#85818E;margin:2px 0 18px}
.card{background:#FFFFFF;border:1px solid #E5E5E9;border-radius:16px;padding:16px 20px;box-shadow:0 1px 3px rgba(41,38,51,.06);height:100%}
.card .lbl{color:#85818E;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.card .val{font-size:44px;font-weight:700;color:#7042B8;line-height:1.15}.card .val.sm{font-size:22px;color:#292633;margin-top:8px}
.card .hint{color:#85818E;font-size:12px}
.pill{display:inline-block;padding:3px 12px;border-radius:999px;font-size:13px;font-weight:600;background:#EFE8F8;color:#593193}
.pill.off{background:#EEEEF1;color:#85818E}.pill.err{background:#F3E3E8;color:#9A2E4B}
.vid{background:#FFFFFF;border:1px solid #E5E5E9;border-radius:16px;padding:10px;box-shadow:0 1px 3px rgba(41,38,51,.06)}
.vid img{width:100%;border-radius:10px;display:block}.vid .empty{padding:70px 10px;text-align:center;color:#85818E}
div.stButton>button,div.stDownloadButton>button{border-radius:10px;border:1px solid #7042B8;font-weight:600}
div.stButton>button[kind="primary"],button[data-testid="stBaseButton-primary"]{background:#7042B8;color:#fff;border-color:#7042B8}
div.stButton>button[kind="primary"]:hover,button[data-testid="stBaseButton-primary"]:hover{background:#593193;border-color:#593193;color:#fff}
div.stButton>button[kind="secondary"],button[data-testid="stBaseButton-secondary"]{background:#fff;color:#7042B8}
div.stButton>button[kind="secondary"]:hover,button[data-testid="stBaseButton-secondary"]:hover{background:#EFE8F8;color:#593193;border-color:#593193}
.stTabs [aria-selected="true"]{color:#7042B8}
.panel{background:#FFFFFF;border:1px solid #E5E5E9;border-radius:16px;padding:6px 18px 14px;margin-bottom:14px}
</style>"""
def apply(): st.markdown(CSS, unsafe_allow_html=True)
def title(t, sub=""): st.markdown(f'<div class="page-title">{t}</div><div class="page-sub">{sub}</div>', unsafe_allow_html=True)
def card(label, value, hint="", small=False):
    return f'<div class="card"><div class="lbl">{label}</div><div class="val{" sm" if small else ""}">{value}</div><div class="hint">{hint}</div></div>'
