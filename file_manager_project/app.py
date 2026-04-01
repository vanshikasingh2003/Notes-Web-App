from __future__ import annotations

import streamlit as st

from file_ops import createfile, deletefile, fileinfo, readfile, readfileandfolder, updatefile
from folder_ops import createfolder, deletefolder, renameitem
from search_ops import searchfiles
from settings import load_settings
from utils import BASE_DIR, ensure_base_dir, get_safe_path, to_relative


st.set_page_config(page_title="Sandboxed File Manager & Notes App", layout="wide")

ensure_base_dir()
settings = load_settings()
show_hidden = bool(settings.get("show_hidden_files", False))
default_ext = str(settings.get("default_extension", ".txt"))

st.markdown(
    """
    <style>
        .stApp {
            background: #0b0f19;
            color: #e5e7eb;
        }
        [data-testid="stHeader"] {
            background: #0b0f19;
        }
        [data-testid="stSidebar"] {
            background: #111827;
        }
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }
        .panel {
            background: #111827;
            border: 1px solid #2a3346;
            border-radius: 12px;
            padding: 1rem 1rem 0.75rem 1rem;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
            margin-bottom: 0.8rem;
        }
        .app-title {
            color: #93c5fd;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .muted {
            color: #9ca3af;
            font-size: 0.95rem;
        }
        .stButton > button {
            border-radius: 10px;
            border: 1px solid #374151;
            background: #1f2937;
            color: #e5e7eb;
        }
        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: #d1d5db !important;
        }
        .stMarkdown, .stCaption, .stSubheader {
            color: #e5e7eb !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="app-title">📂 Sandboxed File Manager & Notes App</h1>', unsafe_allow_html=True)
st.markdown(
    f'<p class="muted">All operations are restricted to sandbox: <code>{BASE_DIR}</code></p>',
    unsafe_allow_html=True,
)

items_for_metrics = readfileandfolder(show_hidden_files=show_hidden)
total_items = len(items_for_metrics)
total_files = sum(1 for p in items_for_metrics if p.is_file())
total_dirs = sum(1 for p in items_for_metrics if p.is_dir())

m1, m2, m3, m4 = st.columns(4)
m1.metric("Items", total_items)
m2.metric("Files", total_files)
m3.metric("Folders", total_dirs)
m4.metric("Default Ext", default_ext)

menu = st.sidebar.selectbox(
    "Select Action",
    [
        "List Files",
        "Create File",
        "Read File",
        "Update File",
        "Delete File",
        "Upload File",
        "Download File",
        "Notes Editor",
        "Search",
        "File Info",
    ],
)

if menu == "List Files":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📋 Files & Folders")
    st.caption("Browse all sandbox items.")
    items = readfileandfolder(show_hidden_files=show_hidden)
    if not items:
        st.info("No files/folders found.")
    else:
        for item in items:
            icon = "📁" if item.is_dir() else "📄"
            st.write(f"{icon} `{to_relative(item)}`")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Create File":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📝 Create File")
    c1, c2 = st.columns([2, 3])
    with c1:
        name = st.text_input("File path")
    with c2:
        content = st.text_area("Initial content (optional)")
    if st.button("Create"):
        final_name = name.strip()
        if final_name and "." not in final_name.split("/")[-1]:
            final_name += default_ext
        ok, msg = createfile(final_name, content)
        st.success(msg) if ok else st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Read File":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📖 Read File")
    name = st.text_input("File path to read")
    if st.button("Read"):
        ok, data = readfile(name)
        if ok:
            st.text_area("Content", data, height=320)
        else:
            st.error(data)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Update File":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("➕ Append to File")
    name = st.text_input("File path to append")
    content = st.text_area("Content to append")
    if st.button("Append"):
        ok, msg = updatefile(name, content)
        st.success(msg) if ok else st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Delete File":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🗑️ Delete File")
    name = st.text_input("File path to delete")
    if st.button("Delete"):
        ok, msg = deletefile(name)
        st.success(msg) if ok else st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Upload File":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📤 Upload File")
    upload_path = st.text_input("Save as path (e.g. uploads/a.txt)")
    uploaded = st.file_uploader("Choose file")
    if st.button("Upload"):
        if not uploaded:
            st.error("Please choose a file.")
        else:
            ok, safe_path, err = get_safe_path(upload_path)
            if not ok or safe_path is None:
                st.error(err)
            else:
                safe_path.parent.mkdir(parents=True, exist_ok=True)
                safe_path.write_bytes(uploaded.getbuffer())
                st.success(f"Uploaded to {to_relative(safe_path)}")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Download File":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📥 Download File")
    name = st.text_input("File path to download")
    if st.button("Load for Download"):
        ok, p, err = get_safe_path(name)
        if not ok or p is None:
            st.error(err)
        elif not p.exists() or not p.is_file():
            st.error("File does not exist.")
        else:
            st.download_button(
                label="Download file",
                data=p.read_bytes(),
                file_name=p.name,
                mime="application/octet-stream",
            )
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Notes Editor":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🗒️ Notes Editor")
    note_name = st.text_input("Note file path", value=f"notes/my_note{default_ext}")
    ok, content = readfile(note_name)
    existing = content if ok else ""
    note_text = st.text_area("Edit note", value=existing, height=260)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Note"):
            ok2, p, err = get_safe_path(note_name)
            if not ok2 or p is None:
                st.error(err)
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(note_text, encoding="utf-8")
                st.success("Note saved.")
    with col2:
        st.markdown("### Markdown Preview")
        st.markdown(note_text)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Search":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🔎 Search")
    pattern = st.text_input("Name or pattern (e.g. *.txt)")
    if st.button("Search"):
        ok, result = searchfiles(pattern, show_hidden_files=show_hidden)
        if not ok:
            st.error(result)
        else:
            if not result:
                st.info("No matches found.")
            for item in result:
                st.write(f"- `{item}`")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "File Info":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("ℹ️ File Info")
    name = st.text_input("File/folder path")
    if st.button("Show Info"):
        ok, result = fileinfo(name)
        if not ok:
            st.error(result)
        else:
            st.json(result)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Folder Operations")
folder_name = st.sidebar.text_input("Folder path")
if st.sidebar.button("Create Folder"):
    ok, msg = createfolder(folder_name)
    st.sidebar.success(msg) if ok else st.sidebar.error(msg)

if st.sidebar.button("Delete Folder"):
    ok, msg = deletefolder(folder_name)
    st.sidebar.success(msg) if ok else st.sidebar.error(msg)

old_name = st.sidebar.text_input("Rename from")
new_name = st.sidebar.text_input("Rename to")
if st.sidebar.button("Rename Item"):
    ok, msg = renameitem(old_name, new_name)
    st.sidebar.success(msg) if ok else st.sidebar.error(msg)
