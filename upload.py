import os
import time
import subprocess
from pathlib import Path
from urllib.parse import quote

# =====================================================
# PATHS
# =====================================================

REPO_FOLDER = Path(r"C:\Users\Mahith Chowdary\Downloads\cine-gallery")

MEDIA_FOLDER = REPO_FOLDER / "media"
PHOTOS_FOLDER = REPO_FOLDER / "photos"
VIDEOS_FOLDER = REPO_FOLDER / "videos"

# Any other folder directly inside the repo becomes a
# top-level section in the left sidebar.
EXCLUDED_ROOT_FOLDERS = {
    ".git", ".github", "__pycache__", "media", "photos", "videos"
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".avif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".avi", ".mkv", ".m4v"}
HTML_EXTENSIONS = {".html", ".htm"}
IGNORED_EXTENSIONS = {".pyc"}

# =====================================================
# FOLDER SETUP
# =====================================================

for folder in (MEDIA_FOLDER, PHOTOS_FOLDER, VIDEOS_FOLDER):
    folder.mkdir(parents=True, exist_ok=True)


# =====================================================
# HELPERS
# =====================================================

def is_media_file(path: Path):
    return path.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS


def classify_file(path: Path):
    ext = path.suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in HTML_EXTENSIONS:
        return "html"
    if ext == ".part":
        return "part"
    return "file"


def safe_name(path: Path):
    return quote(path.name, safe="")


def relative_web_path(path: Path):
    # GitHub Pages uses forward slashes.
    return quote(path.relative_to(REPO_FOLDER).as_posix(), safe="/")


def pretty_name(name: str):
    return name.replace("_", " ").replace("-", " ").strip()


def scan_tree(root: Path):
    """
    Recursively scan a folder.

    Returns:
      {
        "name": folder display name,
        "path": repo-relative path,
        "files": [...],
        "folders": [...]
      }

    Every file is retained. Images/videos render in the gallery;
    HTML/PART/other files appear in a file list.
    """
    node = {
        "name": root.name,
        "path": root.relative_to(REPO_FOLDER).as_posix(),
        "files": [],
        "folders": []
    }

    try:
        children = sorted(
            root.iterdir(),
            key=lambda p: (not p.is_dir(), p.name.lower())
        )
    except OSError:
        return node

    for child in children:
        if child.name.startswith(".") and child.name != ".part":
            continue
        if child.is_dir():
            node["folders"].append(scan_tree(child))
            continue

        if child.suffix.lower() in IGNORED_EXTENSIONS:
            continue

        node["files"].append({
            "name": child.name,
            "path": child.relative_to(REPO_FOLDER).as_posix(),
            "kind": classify_file(child)
        })

    return node


def get_legacy_media():
    photos = []
    videos = []

    for folder, folder_type in (
        (MEDIA_FOLDER, "media"),
        (PHOTOS_FOLDER, "photos"),
        (VIDEOS_FOLDER, "videos"),
    ):
        if not folder.exists():
            continue

        for file in folder.iterdir():
            if not file.is_file():
                continue

            kind = classify_file(file)

            if kind == "image":
                photos.append(file)
            elif kind == "video":
                videos.append(file)

    photos.sort(key=lambda p: p.name.lower())
    videos.sort(key=lambda p: p.name.lower())

    return photos, videos


def get_collection_trees():
    collections = []

    for child in sorted(REPO_FOLDER.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name in EXCLUDED_ROOT_FOLDERS:
            continue
        if child.name.startswith("."):
            continue

        collections.append(scan_tree(child))

    return collections


def flatten_tree_files(node):
    result = list(node["files"])
    for folder in node["folders"]:
        result.extend(flatten_tree_files(folder))
    return result


# =====================================================
# JAVASCRIPT DATA
# =====================================================

def js_quote(value):
    # JSON is valid JavaScript string syntax.
    import json
    return json.dumps(value, ensure_ascii=False)


def build_tree_js(node):
    files = []
    for item in node["files"]:
        files.append(
            "{"
            f"name:{js_quote(item['name'])},"
            f"path:{js_quote(item['path'])},"
            f"kind:{js_quote(item['kind'])}"
            "}"
        )

    folders = [build_tree_js(folder) for folder in node["folders"]]

    return (
        "{"
        f"name:{js_quote(node['name'])},"
        f"path:{js_quote(node['path'])},"
        f"files:[{','.join(files)}],"
        f"folders:[{','.join(folders)}]"
        "}"
    )


# =====================================================
# CREATE WEBSITE
# =====================================================

def create_website():
    photos, videos = get_legacy_media()
    collections = get_collection_trees()

    legacy_files = []

    for file in photos:
        legacy_files.append({
            "name": file.name,
            "path": file.relative_to(REPO_FOLDER).as_posix(),
            "kind": "image"
        })

    for file in videos:
        legacy_files.append({
            "name": file.name,
            "path": file.relative_to(REPO_FOLDER).as_posix(),
            "kind": "video"
        })

    legacy_files_js = ",".join(
        "{"
        f"name:{js_quote(x['name'])},"
        f"path:{js_quote(x['path'])},"
        f"kind:{js_quote(x['kind'])}"
        "}"
        for x in legacy_files
    )

    collections_js = ",".join(build_tree_js(x) for x in collections)

    photo_count = len(photos)
    video_count = len(videos)
    collection_file_count = sum(
        len(flatten_tree_files(x)) for x in collections
    )
    total_count = photo_count + video_count + collection_file_count

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cine Gallery</title>

<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    background: #0f0f0f;
    color: white;
    min-height: 100vh;
}}

.sidebar {{
    position: fixed;
    left: 0;
    top: 0;
    width: 270px;
    height: 100vh;
    background: #151515;
    border-right: 1px solid #292929;
    padding: 25px 14px;
    display: flex;
    flex-direction: column;
    z-index: 100;
    overflow-y: auto;
}}

.logo {{
    text-align: center;
    margin-bottom: 25px;
}}

.logo h1 {{
    font-size: 25px;
    margin-bottom: 7px;
}}

.logo p {{
    color: #777;
    font-size: 12px;
}}

.nav button,
.folder-button {{
    width: 100%;
    border: none;
    background: transparent;
    color: #999;
    padding: 12px 13px;
    margin-bottom: 5px;
    border-radius: 9px;
    text-align: left;
    font-size: 14px;
    cursor: pointer;
    transition: .2s;
}}

.nav button:hover,
.folder-button:hover {{
    background: #222;
    color: white;
}}

.nav button.active,
.folder-button.active {{
    background: #2a2a2a;
    color: white;
}}

.section {{
    margin-top: 18px;
}}

.section-title {{
    color: #666;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 8px 12px;
}}

.folder-tree {{
    padding-left: 5px;
}}

.folder-children {{
    display: none;
    padding-left: 13px;
}}

.folder-children.open {{
    display: block;
}}

.folder-row {{
    display: flex;
    align-items: center;
    gap: 3px;
}}

.folder-toggle {{
    width: 28px;
    border: 0;
    background: transparent;
    color: #777;
    cursor: pointer;
    padding: 8px 0;
}}

.folder-button {{
    flex: 1;
    margin-bottom: 2px;
}}

.stats {{
    margin-top: auto;
    border-top: 1px solid #292929;
    padding-top: 15px;
}}

.stat {{
    display: flex;
    justify-content: space-between;
    padding: 7px 5px;
    color: #777;
    font-size: 12px;
}}

.stat strong {{
    color: white;
}}

.main {{
    margin-left: 270px;
    padding: 42px;
}}

.page-header {{
    margin-bottom: 30px;
}}

.page-header h2 {{
    font-size: 31px;
    margin-bottom: 7px;
}}

.page-header p {{
    color: #777;
}}

.breadcrumb {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 14px;
    color: #666;
    font-size: 12px;
}}

.breadcrumb span {{
    color: #aaa;
}}

.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 22px;
}}

.card {{
    background: #181818;
    padding: 8px;
    border-radius: 16px;
    overflow: hidden;
}}

.card img {{
    width: 100%;
    height: 350px;
    object-fit: cover;
    display: block;
    border-radius: 11px;
}}

.card video {{
    width: 100%;
    height: 350px;
    object-fit: cover;
    display: block;
    border-radius: 11px;
    background: #000;
}}

.file-list {{
    display: grid;
    gap: 10px;
    margin-top: 28px;
}}

.file-card {{
    background: #181818;
    border: 1px solid #242424;
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
}}

.file-info {{
    min-width: 0;
}}

.file-name {{
    font-size: 14px;
    overflow-wrap: anywhere;
}}

.file-type {{
    color: #666;
    font-size: 11px;
    margin-top: 4px;
    text-transform: uppercase;
}}

.file-link {{
    flex-shrink: 0;
    color: white;
    background: #292929;
    text-decoration: none;
    border-radius: 8px;
    padding: 8px 11px;
    font-size: 12px;
}}

.file-link:hover {{
    background: #3a3a3a;
}}

.empty {{
    color: #666;
    padding: 25px 0;
}}

@media (max-width: 700px) {{
    .sidebar {{
        width: 78px;
        padding: 18px 7px;
    }}

    .logo h1 {{
        font-size: 0;
    }}

    .logo h1::after {{
        content: "🎬";
        font-size: 25px;
    }}

    .logo p,
    .section-title,
    .stats,
    .folder-toggle {{
        display: none;
    }}

    .nav button,
    .folder-button {{
        text-align: center;
        font-size: 0;
        padding: 12px 5px;
    }}

    .folder-button::before {{
        content: "📁";
        font-size: 18px;
    }}

    .main {{
        margin-left: 78px;
        padding: 25px 15px;
    }}

    .gallery {{
        grid-template-columns: 1fr;
    }}
}}
</style>
</head>

<body>

<aside class="sidebar">

<div class="logo">
    <h1>🎬 Cine Gallery</h1>
    <p>My Collection</p>
</div>

<div class="nav">
    <button class="active" onclick="openLegacy('photos', this)">
        🖼️ &nbsp; Photos
    </button>

    <button onclick="openLegacy('videos', this)">
        🎥 &nbsp; Videos
    </button>
</div>

<div class="section">
    <div class="section-title">Collections</div>
    <div id="folderTree" class="folder-tree"></div>
</div>

<div class="stats">
    <div class="stat">
        <span>Total</span>
        <strong>{total_count}</strong>
    </div>
    <div class="stat">
        <span>Photos</span>
        <strong>{photo_count}</strong>
    </div>
    <div class="stat">
        <span>Videos</span>
        <strong>{video_count}</strong>
    </div>
    <div class="stat">
        <span>Collection files</span>
        <strong>{collection_file_count}</strong>
    </div>
</div>

</aside>

<main class="main">

<div class="page-header">
    <h2 id="pageTitle">Photos</h2>
    <p id="pageDescription">My photo collection</p>
    <div id="breadcrumb" class="breadcrumb"></div>
</div>

<div id="content"></div>

</main>

<script>
const legacyFiles = [{legacy_files_js}];
const collections = [{collections_js}];

function fileUrl(path) {{
    return path.split("/").map(encodeURIComponent).join("/");
}}

function escapeHtml(value) {{
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}}

function setActive(element) {{
    document.querySelectorAll(".nav button, .folder-button")
        .forEach(x => x.classList.remove("active"));
    if (element) element.classList.add("active");
}}

function renderMedia(files) {{
    const content = document.getElementById("content");
    const media = files.filter(x => x.kind === "image" || x.kind === "video");
    const other = files.filter(x => x.kind !== "image" && x.kind !== "video");

    if (!media.length && !other.length) {{
        content.innerHTML = '<div class="empty">This folder is empty.</div>';
        return;
    }}

    let html = "";

    if (media.length) {{
        html += '<div class="gallery">';

        media.forEach(item => {{
            const url = fileUrl(item.path);

            if (item.kind === "image") {{
                html += `
                <div class="card">
                    <img src="${{url}}" alt="${{escapeHtml(item.name)}}" loading="lazy">
                </div>`;
            }} else {{
                html += `
                <div class="card">
                    <video controls preload="none" playsinline>
                        <source src="${{url}}">
                        Your browser does not support video.
                    </video>
                </div>`;
            }}
        }});

        html += "</div>";
    }}

    if (other.length) {{
        html += '<div class="file-list">';

        other.forEach(item => {{
            const url = fileUrl(item.path);
            const label =
                item.kind === "html" ? "HTML" :
                item.kind === "part" ? "PART / INCOMPLETE" :
                "FILE";

            html += `
            <div class="file-card">
                <div class="file-info">
                    <div class="file-name">${{escapeHtml(item.name)}}</div>
                    <div class="file-type">${{label}}</div>
                </div>
                <a class="file-link"
                   href="${{url}}"
                   target="_blank"
                   rel="noopener">
                   Open
                </a>
            </div>`;
        }});

        html += "</div>";
    }}

    content.innerHTML = html;
}}

function setHeader(title, description, pathParts=[]) {{
    document.getElementById("pageTitle").innerText = title;
    document.getElementById("pageDescription").innerText = description;

    const breadcrumb = document.getElementById("breadcrumb");

    if (!pathParts.length) {{
        breadcrumb.innerHTML = "";
        return;
    }}

    breadcrumb.innerHTML = pathParts
        .map(x => `<span>› ${{escapeHtml(x)}}</span>`)
        .join("");
}}

function openLegacy(type, button) {{
    setActive(button);

    if (type === "photos") {{
        const files = legacyFiles.filter(x => x.kind === "image");
        setHeader("Photos", "My photo collection");
        renderMedia(files);
    }} else {{
        const files = legacyFiles.filter(x => x.kind === "video");
        setHeader("Videos", "My video collection");
        renderMedia(files);
    }}
}}

function findFolderByPath(root, targetPath) {{
    if (root.path === targetPath) return root;

    for (const child of root.folders) {{
        const found = findFolderByPath(child, targetPath);
        if (found) return found;
    }}

    return null;
}}

function openFolder(folder, button) {{
    setActive(button);

    const allFiles = [...folder.files];

    // A folder page shows files directly inside it.
    // Subfolders are shown as folders in the sidebar.
    const parts = folder.path.split("/");

    setHeader(
        folder.name,
        "Folder contents",
        parts
    );

    renderMedia(allFiles);
}}

function buildFolderNode(folder) {{
    const wrapper = document.createElement("div");

    const row = document.createElement("div");
    row.className = "folder-row";

    const toggle = document.createElement("button");
    toggle.className = "folder-toggle";
    toggle.innerText = folder.folders.length ? "›" : "";

    const button = document.createElement("button");
    button.className = "folder-button";
    button.innerText = "📁 " + folder.name;

    button.onclick = () => openFolder(folder, button);

    row.appendChild(toggle);
    row.appendChild(button);
    wrapper.appendChild(row);

    if (folder.folders.length) {{
        const children = document.createElement("div");
        children.className = "folder-children";

        folder.folders.forEach(child => {{
            children.appendChild(buildFolderNode(child));
        }});

        toggle.onclick = () => {{
            children.classList.toggle("open");
            toggle.innerText =
                children.classList.contains("open") ? "⌄" : "›";
        }};

        wrapper.appendChild(children);
    }}

    return wrapper;
}}

function buildSidebar() {{
    const root = document.getElementById("folderTree");
    root.innerHTML = "";

    collections.forEach(collection => {{
        root.appendChild(buildFolderNode(collection));
    }});
}}

buildSidebar();
openLegacy("photos", document.querySelector(".nav button"));
</script>

</body>
</html>
"""

    index_file = REPO_FOLDER / "index.html"

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html)

    print()
    print("Website updated!")
    print()
    print(f"Legacy photos:       {photo_count}")
    print(f"Legacy videos:       {video_count}")
    print(f"Collection files:    {collection_file_count}")
    print(f"Total files:         {total_count}")
    print(f"Collections:         {len(collections)}")
    print()


# =====================================================
# GIT PUSH
# =====================================================

def push_to_github():
    os.chdir(REPO_FOLDER)

    subprocess.run(["git", "add", "."], check=True)

    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    )

    if result.returncode == 0:
        print("No changes to push.")
        return

    subprocess.run(
        ["git", "commit", "-m", "Update gallery"],
        check=True
    )

    subprocess.run(
        ["git", "push", "origin", "main"],
        check=True
    )

    print("✅ Successfully pushed to GitHub!")


# =====================================================
# GET COMPLETE FOLDER STATE
# =====================================================

def get_folder_state():
    state = {}

    for path in REPO_FOLDER.rglob("*"):
        if not path.is_file():
            continue

        # Ignore Git internals and generated Python cache.
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue

        try:
            stat = path.stat()
            state[path.relative_to(REPO_FOLDER).as_posix()] = (
                stat.st_size,
                stat.st_mtime_ns
            )
        except OSError:
            pass

    return state


# =====================================================
# START
# =====================================================

print()
print("======================================")
print("       CINE GALLERY AUTOMATION")
print("======================================")
print()
print("Repository:")
print(REPO_FOLDER)
print()
print("Create collection folders directly inside:")
print(REPO_FOLDER)
print()
print("Example:")
print(REPO_FOLDER / "Naga Chaitanya" / "SIIMA")
print()
print("Supported:")
print("  Images  -> gallery")
print("  Videos  -> playable gallery")
print("  HTML    -> openable file")
print("  .part   -> listed as incomplete file")
print("  Other   -> listed as file")
print()
print("Watching repository recursively...")
print("Press CTRL + C to stop.")
print()

create_website()
push_to_github()

old_state = get_folder_state()

while True:
    try:
        time.sleep(10)

        new_state = get_folder_state()

        if old_state != new_state:
            print()
            print("📁 Change detected!")
            print()

            create_website()
            push_to_github()

            old_state = new_state

            print()

    except KeyboardInterrupt:
        print()
        print("Automation stopped.")
        break

    except Exception as error:
        print()
        print("ERROR:")
        print(error)
        print()
        time.sleep(10)
