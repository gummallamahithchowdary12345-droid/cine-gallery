import os
import time
import subprocess
from pathlib import Path
from urllib.parse import quote


# =====================================================
# PATHS
# =====================================================

REPO_FOLDER = r"C:\Users\Mahith Chowdary\Downloads\cine-gallery"

MEDIA_FOLDER = os.path.join(REPO_FOLDER, "media")
PHOTOS_FOLDER = os.path.join(REPO_FOLDER, "photos")
VIDEOS_FOLDER = os.path.join(REPO_FOLDER, "videos")


# =====================================================
# FILE TYPES
# =====================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp"
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".webm",
    ".avi",
    ".mkv"
}

ALL_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS


# =====================================================
# CREATE STANDARD FOLDERS
# =====================================================

os.makedirs(MEDIA_FOLDER, exist_ok=True)
os.makedirs(PHOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)


# =====================================================
# GET STANDARD MEDIA
# =====================================================

def get_media():

    photos = []
    videos = []

    # -------------------------------------------------
    # MEDIA
    # -------------------------------------------------

    for file in Path(MEDIA_FOLDER).iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension in IMAGE_EXTENSIONS:

            photos.append(
                (file, "media")
            )

        elif extension in VIDEO_EXTENSIONS:

            videos.append(
                (file, "media")
            )

    # -------------------------------------------------
    # PHOTOS
    # -------------------------------------------------

    for file in Path(PHOTOS_FOLDER).iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() in IMAGE_EXTENSIONS:

            photos.append(
                (file, "photos")
            )

    # -------------------------------------------------
    # VIDEOS
    # -------------------------------------------------

    for file in Path(VIDEOS_FOLDER).iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() in VIDEO_EXTENSIONS:

            videos.append(
                (file, "videos")
            )

    # -------------------------------------------------
    # SORT
    # -------------------------------------------------

    photos.sort(
        key=lambda x: x[0].name.lower()
    )

    videos.sort(
        key=lambda x: x[0].name.lower()
    )

    return photos, videos


# =====================================================
# GET WEBSITE PATH
# =====================================================

def get_web_path(file, folder_type):

    filename = quote(file.name)

    return f"{folder_type}/{filename}"


# =====================================================
# GET CUSTOM TOP-LEVEL FOLDERS
#
# Example:
#
# chay/
#     SIIMA/
#     Events/
#     Thandel/
#
# =====================================================

def get_custom_folders():

    folders = []

    root = Path(REPO_FOLDER)

    ignored_folders = {
        ".git",
        ".github",
        "__pycache__",
        "media",
        "photos",
        "videos"
    }

    for item in root.iterdir():

        if not item.is_dir():
            continue

        if item.name in ignored_folders:
            continue

        folders.append(item)

    folders.sort(
        key=lambda x: x.name.lower()
    )

    return folders


# =====================================================
# GET ALL FOLDERS RECURSIVELY
# =====================================================

def get_all_custom_folders():

    all_folders = []

    for root_folder in get_custom_folders():

        # Add top-level folder
        all_folders.append(root_folder)

        # Add every nested folder
        for folder in root_folder.rglob("*"):

            if folder.is_dir():

                all_folders.append(folder)

    return all_folders


# =====================================================
# GET CHILD FOLDERS
# =====================================================

def get_child_folders(folder):

    children = []

    try:

        for item in folder.iterdir():

            if item.is_dir():

                children.append(item)

    except Exception:
        pass

    children.sort(
        key=lambda x: x.name.lower()
    )

    return children


# =====================================================
# GET ALL MEDIA INSIDE FOLDER
#
# IMPORTANT:
# This is recursive.
#
# So:
#
# chay/SIIMA/video.mp4
#
# WILL BE FOUND.
#
# =====================================================

def get_folder_media(folder):

    media = []

    try:

        # IMPORTANT:
        # Only look at files directly inside this folder.
        # Do NOT search inside child folders.

        for file in folder.iterdir():

            if not file.is_file():
                continue

            if file.suffix.lower() not in ALL_EXTENSIONS:
                continue

            relative_path = file.relative_to(
                Path(REPO_FOLDER)
            )

            media.append(
                (
                    file,
                    relative_path
                )
            )

    except Exception:
        pass

    media.sort(
        key=lambda x: str(x[0]).lower()
    )

    return media

# =====================================================
# GET CUSTOM WEB PATH
# =====================================================

def get_custom_web_path(file):

    relative = file.relative_to(
        Path(REPO_FOLDER)
    )

    parts = []

    for part in relative.parts:

        parts.append(
            quote(part)
        )

    return "/".join(parts)


# =====================================================
# CREATE FOLDER HTML
# =====================================================

def create_folder_html(folder):

    html = ""

    # =================================================
    # CHILD FOLDERS
    # =================================================

    child_folders = get_child_folders(folder)

    if child_folders:

        html += """
<div class="folder-grid">
"""


        for child in child_folders:

            relative = child.relative_to(
                Path(REPO_FOLDER)
            )

            folder_id = "/".join(
                relative.parts
            )

            encoded_id = quote(
                folder_id,
                safe=""
            )

            child_media = get_folder_media(
                child
            )

            html += f"""
<div
    class="folder-card"
    onclick="showCustomFolder('{encoded_id}')"
>

    <div class="folder-icon">
        📁
    </div>

    <div class="folder-name">
        {child.name}
    </div>

    <div class="folder-count">
        {len(child_media)} items
    </div>

</div>
"""


        html += """
</div>
"""


    # =================================================
    # MEDIA
    # =================================================

    media = get_folder_media(folder)

    if media:

        html += """
<div class="gallery">
"""


        for file, relative_path in media:

            web_path = get_custom_web_path(
                file
            )

            extension = file.suffix.lower()


            # -----------------------------------------
            # IMAGE
            # -----------------------------------------

            if extension in IMAGE_EXTENSIONS:

                html += f"""
<div class="card">

<img
    src="{web_path}"
    alt="Photo"
    loading="lazy"
    decoding="async">

</div>
"""


            # -----------------------------------------
            # VIDEO
            # -----------------------------------------

            elif extension in VIDEO_EXTENSIONS:

                html += f"""
<div class="card">

<video
    controls
    preload="metadata"
    playsinline>

<source
    src="{web_path}">

Your browser does not support video.

</video>

</div>
"""


        html += """
</div>
"""


    # =================================================
    # EMPTY
    # =================================================

    if not child_folders and not media:

        html += """
<p style="
    color:#777;
    padding:20px 0;
">
    This folder is empty.
</p>
"""


    return html


# =====================================================
# CREATE SIDEBAR FOLDERS
# =====================================================

def create_sidebar_folders():

    folders = get_custom_folders()

    html = ""

    for folder in folders:

        relative = folder.relative_to(
            Path(REPO_FOLDER)
        )

        folder_id = "/".join(
            relative.parts
        )

        encoded_id = quote(
            folder_id,
            safe=""
        )

        html += f"""
<button
    onclick="showCustomFolder('{encoded_id}', this)">
    📁 {folder.name}
</button>
"""


    return html


# =====================================================
# CREATE WEBSITE
# =====================================================

def create_website():

    photos, videos = get_media()

    photo_count = len(photos)
    video_count = len(videos)
    total_count = photo_count + video_count

    custom_folders = get_custom_folders()

    all_custom_folders = get_all_custom_folders()


    # =================================================
    # HTML START
    # =================================================

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0">

<title>Cine Gallery</title>

<style>


/* =================================================
   GENERAL
   ================================================= */

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


/* =================================================
   SIDEBAR
   ================================================= */

.sidebar {{

    position: fixed;

    left: 0;

    top: 0;

    width: 230px;

    height: 100vh;

    background: #151515;

    border-right: 1px solid #292929;

    padding: 30px 15px;

    display: flex;

    flex-direction: column;

    z-index: 100;

}}


/* =================================================
   LOGO
   ================================================= */

.logo {{

    text-align: center;

    margin-bottom: 40px;

}}


.logo h1 {{

    font-size: 27px;

    margin-bottom: 8px;

}}


.logo p {{

    color: #777;

    font-size: 12px;

}}


/* =================================================
   NAVIGATION
   ================================================= */

.nav {{

    overflow-y: auto;

}}


.nav button {{

    width: 100%;

    border: none;

    background: transparent;

    color: #999;

    padding: 14px 16px;

    margin-bottom: 8px;

    border-radius: 10px;

    text-align: left;

    font-size: 15px;

    cursor: pointer;

    transition: 0.2s;

}}


.nav button:hover {{

    background: #222;

    color: white;

}}


.nav button.active {{

    background: #2a2a2a;

    color: white;

}}


/* =================================================
   STATS
   ================================================= */

.stats {{

    margin-top: auto;

    border-top: 1px solid #292929;

    padding-top: 20px;

}}


.stat {{

    display: flex;

    justify-content: space-between;

    padding: 8px 5px;

    color: #777;

    font-size: 13px;

}}


.stat strong {{

    color: white;

}}


/* =================================================
   MAIN
   ================================================= */

.main {{

    margin-left: 230px;

    padding: 45px;

}}


/* =================================================
   HEADER
   ================================================= */

.page-header {{

    margin-bottom: 35px;

}}


.page-header h2 {{

    font-size: 32px;

    margin-bottom: 8px;

}}


.page-header p {{

    color: #777;

}}


/* =================================================
   GALLERY
   ================================================= */

.gallery {{

    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(280px, 1fr)
        );

    gap: 22px;

}}


/* =================================================
   CARD
   ================================================= */

.card {{

    background: #181818;

    padding: 8px;

    border-radius: 16px;

    overflow: hidden;

}}


/* =================================================
   IMAGES
   ================================================= */

.card img {{

    width: 100%;

    height: 350px;

    object-fit: cover;

    display: block;

    border-radius: 11px;

}}


/* =================================================
   VIDEOS
   ================================================= */

.card video {{

    width: 100%;

    height: 350px;

    object-fit: cover;

    display: block;

    border-radius: 11px;

    background: #000;

}}


/* =================================================
   FOLDERS
   ================================================= */

.folder-grid {{

    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(220px, 1fr)
        );

    gap: 22px;

    margin-bottom: 35px;

}}


.folder-card {{

    background: #181818;

    padding: 25px;

    border-radius: 16px;

    border: 1px solid #292929;

    cursor: pointer;

    transition: 0.2s;

}}


.folder-card:hover {{

    background: #222;

    border-color: #444;

    transform: translateY(-3px);

}}


.folder-icon {{

    font-size: 45px;

    margin-bottom: 15px;

}}


.folder-name {{

    font-size: 18px;

    font-weight: bold;

    margin-bottom: 8px;

}}


.folder-count {{

    color: #777;

    font-size: 13px;

}}


/* =================================================
   MOBILE
   ================================================= */

@media (max-width: 700px) {{

    .sidebar {{

        width: 75px;

        padding: 20px 8px;

    }}


    .logo h1 {{

        font-size: 0;

    }}


    .logo h1::after {{

        content: "🎬";

        font-size: 25px;

    }}


    .logo p {{

        display: none;

    }}


    .nav button {{

        text-align: center;

        padding: 13px 5px;

        font-size: 0;

    }}


    .stats {{

        display: none;

    }}


    .main {{

        margin-left: 75px;

        padding: 25px 15px;

    }}


    .gallery {{

        grid-template-columns: 1fr;

    }}


    .folder-grid {{

        grid-template-columns: 1fr;

    }}

}}


</style>

</head>


<body>


<!-- =================================================
     SIDEBAR
     ================================================= -->

<aside class="sidebar">


<div class="logo">

<h1>🎬 Cine Gallery</h1>

<p>My Collection</p>

</div>


<div class="nav">


<button
    class="active"
    onclick="showSection('photos', this)">

    🖼️ &nbsp; Photos

</button>


<button
    onclick="showSection('videos', this)">

    🎥 &nbsp; Videos

</button>


{create_sidebar_folders()}


</div>


<!-- =================================================
     COUNTS
     ================================================= -->

<div class="stats">


<div class="stat">

<span>Posts</span>

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


</div>


</aside>


<!-- =================================================
     MAIN
     ================================================= -->

<main class="main">


<div class="page-header">

<h2 id="pageTitle">
Photos
</h2>

<p id="pageDescription">
My photo collection
</p>

</div>


<!-- =================================================
     PHOTOS
     ================================================= -->

<div id="photos">


<div class="gallery">
"""


    # =================================================
    # ADD PHOTOS
    # =================================================

    for file, folder_type in photos:

        web_path = get_web_path(
            file,
            folder_type
        )

        html += f"""
<div class="card">

<img
    src="{web_path}"
    alt="Photo"
    loading="lazy"
    decoding="async">

</div>
"""


    html += """
</div>

</div>


<!-- =================================================
     VIDEOS
     ================================================= -->

<div
    id="videos"
    style="display:none;">

<div class="gallery">
"""


    # =================================================
    # ADD VIDEOS
    # =================================================

    for file, folder_type in videos:

        web_path = get_web_path(
            file,
            folder_type
        )

        html += f"""
<div class="card">

<video
    controls
    preload="none"
    playsinline>

<source
    src="{web_path}">

Your browser does not support video.

</video>

</div>
"""


    html += """
</div>

</div>


<!-- =================================================
     CUSTOM FOLDER
     ================================================= -->

<div
    id="customFolder"
    style="display:none;">

<div id="folderContent">
</div>

</div>


</main>


<!-- =================================================
     JAVASCRIPT
     ================================================= -->

<script>


/* =================================================
   FOLDER DATA
   ================================================= */

const folderData = {
"""


    # =================================================
    # GENERATE DATA FOR EVERY FOLDER
    #
    # THIS IS THE IMPORTANT FIX
    #
    # It includes:
    #
    # chay
    # chay/SIIMA
    # chay/Events
    # chay/Thandel
    #
    # and any deeper folders.
    # =================================================

    for folder in all_custom_folders:

        relative = folder.relative_to(
            Path(REPO_FOLDER)
        )

        folder_id = "/".join(
            relative.parts
        )

        encoded_id = quote(
            folder_id,
            safe=""
        )

        folder_html = create_folder_html(
            folder
        )


        # Escape JavaScript template literal

        folder_html = (
            folder_html
            .replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("${", "\\${")
        )


        html += f"""
"{encoded_id}": `
{folder_html}
`,
"""


    html += """
};


/* =================================================
   SHOW PHOTOS / VIDEOS
   ================================================= */

function showSection(section, button) {

    const photos =
        document.getElementById("photos");

    const videos =
        document.getElementById("videos");

    const customFolder =
        document.getElementById("customFolder");

    const title =
        document.getElementById("pageTitle");

    const description =
        document.getElementById("pageDescription");


    photos.style.display = "none";

    videos.style.display = "none";

    customFolder.style.display = "none";


    document
        .querySelectorAll(".nav button")
        .forEach(btn => {

            btn.classList.remove("active");

        });


    if (button) {

        button.classList.add("active");

    }


    /* ---------------------------------------------
       PHOTOS
       --------------------------------------------- */

    if (section === "photos") {

        photos.style.display = "block";

        title.innerText = "Photos";

        description.innerText =
            "My photo collection";

    }


    /* ---------------------------------------------
       VIDEOS
       --------------------------------------------- */

    if (section === "videos") {

        videos.style.display = "block";

        title.innerText = "Videos";

        description.innerText =
            "My video collection";

    }

}


/* =================================================
   SHOW CUSTOM FOLDER
   ================================================= */

function showCustomFolder(
    folderId,
    button = null
) {

    const photos =
        document.getElementById("photos");

    const videos =
        document.getElementById("videos");

    const customFolder =
        document.getElementById("customFolder");

    const folderContent =
        document.getElementById("folderContent");

    const title =
        document.getElementById("pageTitle");

    const description =
        document.getElementById("pageDescription");


    /* ---------------------------------------------
       Hide normal sections
       --------------------------------------------- */

    photos.style.display = "none";

    videos.style.display = "none";

    customFolder.style.display = "block";


    /* ---------------------------------------------
       Get folder name
       --------------------------------------------- */

    let decodedId = folderId;


    try {

        decodedId =
            decodeURIComponent(folderId);

    }

    catch (error) {

        decodedId =
            folderId;

    }


    const parts =
        decodedId.split("/");


    const folderName =
        parts[parts.length - 1];


    title.innerText =
        folderName;


    description.innerText =
        "Folder collection";


    /* ---------------------------------------------
       Show folder content
       --------------------------------------------- */

    if (folderData[folderId]) {

        folderContent.innerHTML =
            folderData[folderId];

    }

    else {

        folderContent.innerHTML = `
<p style="
    color:#777;
    padding:20px 0;
">
    This folder is empty.
</p>
`;

    }


    /* ---------------------------------------------
       Active sidebar button
       --------------------------------------------- */

    document
        .querySelectorAll(".nav button")
        .forEach(btn => {

            btn.classList.remove("active");

        });


    if (button) {

        button.classList.add("active");

    }

}


</script>


</body>

</html>
"""


    # =================================================
    # SAVE INDEX.HTML
    # =================================================

    index_file = os.path.join(
        REPO_FOLDER,
        "index.html"
    )


    with open(
        index_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)


    print()
    print("Website updated!")
    print()
    print(f"Posts:   {total_count}")
    print(f"Photos:  {photo_count}")
    print(f"Videos:  {video_count}")
    print(f"Folders: {len(custom_folders)}")
    print()


# =====================================================
# GET COMPLETE FOLDER STATE
# =====================================================

def get_folder_state():

    state = {}

    root = Path(REPO_FOLDER)

    ignored = {
        ".git",
        ".github",
        "__pycache__"
    }


    for file in root.rglob("*"):

        if not file.is_file():
            continue


        try:

            relative = file.relative_to(
                root
            )

        except Exception:

            continue


        # Ignore git/system files

        if any(
            part in ignored
            for part in relative.parts
        ):
            continue


        # Ignore generated index

        if file.name == "index.html":
            continue


        try:

            state[
                str(relative)
            ] = (
                file.stat().st_size,
                file.stat().st_mtime
            )

        except Exception:

            pass


    return state


# =====================================================
# GIT PUSH
# =====================================================

def push_to_github():

    os.chdir(REPO_FOLDER)


    # -------------------------------------------------
    # ADD
    # -------------------------------------------------

    subprocess.run(
        [
            "git",
            "add",
            "."
        ],
        check=True
    )


    # -------------------------------------------------
    # CHECK CHANGES
    # -------------------------------------------------

    result = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet"
        ]
    )


    if result.returncode == 0:

        print(
            "No changes to push."
        )

        return


    # -------------------------------------------------
    # COMMIT
    # -------------------------------------------------

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "Update gallery"
        ],
        check=True
    )


    # -------------------------------------------------
    # PUSH
    # -------------------------------------------------

    subprocess.run(
        [
            "git",
            "push",
            "origin",
            "main"
        ],
        check=True
    )


    print(
        "✅ Successfully pushed to GitHub!"
    )


# =====================================================
# START
# =====================================================

print()

print(
    "======================================"
)

print(
    "       CINE GALLERY AUTOMATION"
)

print(
    "======================================"
)

print()

print(
    "Existing media folder:"
)

print(
    MEDIA_FOLDER
)

print()

print(
    "New photos folder:"
)

print(
    PHOTOS_FOLDER
)

print()

print(
    "New videos folder:"
)

print(
    VIDEOS_FOLDER
)

print()

print(
    "Watching all folders..."
)

print(
    "Press CTRL + C to stop."
)

print()


# =====================================================
# FIRST UPDATE
# =====================================================

create_website()

push_to_github()


# =====================================================
# WATCH
# =====================================================

old_state = get_folder_state()


while True:

    try:

        time.sleep(10)

        new_state = get_folder_state()


        if old_state != new_state:

            print()

            print(
                "📸 New media/folder detected!"
            )

            print()


            create_website()

            push_to_github()


            old_state = new_state

            print()


    except KeyboardInterrupt:

        print()

        print(
            "Automation stopped."
        )

        break


    except Exception as error:

        print()

        print(
            "ERROR:"
        )

        print(
            error
        )

        print()

        time.sleep(10)
