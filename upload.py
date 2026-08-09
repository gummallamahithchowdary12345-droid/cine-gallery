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
# CREATE NEW FOLDERS
# =====================================================

os.makedirs(MEDIA_FOLDER, exist_ok=True)
os.makedirs(PHOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)


# =====================================================
# GET ALL MEDIA
# =====================================================

def get_media():

    photos = []
    videos = []

    # -------------------------------------------------
    # OLD MEDIA FOLDER
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
    # NEW PHOTOS FOLDER
    # -------------------------------------------------

    for file in Path(PHOTOS_FOLDER).iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() in IMAGE_EXTENSIONS:

            photos.append(
                (file, "photos")
            )


    # -------------------------------------------------
    # NEW VIDEOS FOLDER
    # -------------------------------------------------

    for file in Path(VIDEOS_FOLDER).iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() in VIDEO_EXTENSIONS:

            videos.append(
                (file, "videos")
            )


    # Sort

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
# CREATE WEBSITE
# =====================================================

def create_website():

    photos, videos = get_media()

    photo_count = len(photos)
    video_count = len(videos)
    total_count = photo_count + video_count


    # =================================================
    # HTML START
    # =================================================

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
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

<div id="videos"
     style="display: none;">


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


</main>


<!-- =================================================
     JAVASCRIPT
     ================================================= -->

<script>


function showSection(section, button) {{

    const photos =
        document.getElementById("photos");

    const videos =
        document.getElementById("videos");


    const title =
        document.getElementById("pageTitle");


    const description =
        document.getElementById(
            "pageDescription"
        );


    // Remove active state

    document
        .querySelectorAll(".nav button")
        .forEach(btn => {{

            btn.classList.remove("active");

        }});


    // Activate clicked button

    button.classList.add("active");


    // =================================================
    // PHOTOS
    // =================================================

    if (section === "photos") {{

        photos.style.display = "block";

        videos.style.display = "none";

        title.innerText = "Photos";

        description.innerText =
            "My photo collection";

    }}


    // =================================================
    // VIDEOS
    // =================================================

    if (section === "videos") {{

        photos.style.display = "none";

        videos.style.display = "block";

        title.innerText = "Videos";

        description.innerText =
            "My video collection";

    }}

}}

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
    print(f"Posts:  {total_count}")
    print(f"Photos: {photo_count}")
    print(f"Videos: {video_count}")
    print()


# =====================================================
# GIT PUSH
# =====================================================

def push_to_github():

    os.chdir(REPO_FOLDER)


    # Add changes

    subprocess.run(
        ["git", "add", "."],
        check=True
    )


    # Check changes

    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    )


    if result.returncode == 0:

        print("No changes to push.")

        return


    # Commit

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "Update gallery"
        ],
        check=True
    )


    # Push

    subprocess.run(
        [
            "git",
            "push",
            "origin",
            "main"
        ],
        check=True
    )


    print("✅ Successfully pushed to GitHub!")


# =====================================================
# GET FOLDER STATE
# =====================================================

def get_folder_state():

    state = {}


    folders = [
        ("media", MEDIA_FOLDER),
        ("photos", PHOTOS_FOLDER),
        ("videos", VIDEOS_FOLDER)
    ]


    for folder_name, folder_path in folders:

        for file in Path(folder_path).iterdir():

            if not file.is_file():
                continue

            state[
                folder_name + "/" + file.name
            ] = (
                file.stat().st_size,
                file.stat().st_mtime
            )


    return state


# =====================================================
# START
# =====================================================

print()

print("======================================")

print("       CINE GALLERY AUTOMATION")

print("======================================")

print()

print("Existing media folder:")

print(MEDIA_FOLDER)

print()

print("New photos folder:")

print(PHOTOS_FOLDER)

print()

print("New videos folder:")

print(VIDEOS_FOLDER)

print()

print("Watching all folders...")

print("Press CTRL + C to stop.")

print()


# =====================================================
# FIRST UPDATE
# =====================================================

create_website()

push_to_github()


# =====================================================
# WATCH
# =====================================================

while True:

    try:

        time.sleep(10)


        old_state = get_folder_state()


        time.sleep(2)


        new_state = get_folder_state()


        if old_state != new_state:

            print()

            print("📸 New media detected!")

            print()

            create_website()

            push_to_github()

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