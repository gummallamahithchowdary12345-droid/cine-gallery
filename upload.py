import os
import time
import subprocess
from pathlib import Path
from urllib.parse import quote


# ==========================================
# PATHS
# ==========================================

REPO_FOLDER = r"C:\Users\Mahith Chowdary\Downloads\cine-gallery"

MEDIA_FOLDER = r"C:\Users\Mahith Chowdary\Downloads\cine-gallery\media"


# ==========================================
# FILE TYPES
# ==========================================

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


# ==========================================
# CREATE WEBSITE
# ==========================================

def create_website():

    files = []

    for file in Path(MEDIA_FOLDER).iterdir():

        if (
            file.is_file()
            and file.suffix.lower() in ALL_EXTENSIONS
        ):
            files.append(file)

    files.sort(key=lambda x: x.name.lower())


    # Separate images and videos

    images = [
        file for file in files
        if file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    videos = [
        file for file in files
        if file.suffix.lower() in VIDEO_EXTENSIONS
    ]


    post_count = len(files)
    image_count = len(images)
    video_count = len(videos)


    # ==========================================
    # HTML
    # ==========================================

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Cine Gallery</title>


<style>

/* ==========================================
   GENERAL
   ========================================== */

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


/* ==========================================
   SIDEBAR
   ========================================== */

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


/* LOGO */

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


/* ==========================================
   NAVIGATION
   ========================================== */

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


/* ==========================================
   STATS
   ========================================== */

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


/* ==========================================
   MAIN
   ========================================== */

.main {{

    margin-left: 230px;

    padding: 45px;

}}


/* ==========================================
   HEADER
   ========================================== */

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


/* ==========================================
   GALLERY
   ========================================== */

.gallery {{

    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(280px, 1fr)
        );

    gap: 22px;

}}


/* ==========================================
   CARD
   ========================================== */

.card {{

    background: #181818;

    padding: 8px;

    border-radius: 16px;

    overflow: hidden;

    contain: content;

}}


/* ==========================================
   IMAGES
   ========================================== */

.card img {{

    width: 100%;

    height: 350px;

    object-fit: cover;

    display: block;

    border-radius: 11px;

}}


/* ==========================================
   VIDEOS
   ========================================== */

.card video {{

    width: 100%;

    height: 350px;

    object-fit: cover;

    display: block;

    border-radius: 11px;

    background: #000;

}}


/* ==========================================
   SECTION
   ========================================== */

.section-title {{

    font-size: 25px;

    margin-bottom: 25px;

    border-left: 4px solid #777;

    padding-left: 12px;

}}


/* ==========================================
   MOBILE
   ========================================== */

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


<!-- ==========================================
     SIDEBAR
     ========================================== -->

<aside class="sidebar">


<div class="logo">

<h1>🎬 Cine Gallery</h1>

<p>My Collection</p>

</div>


<div class="nav">


<button
    class="active"
    onclick="showMedia('image', this)">

🖼️ &nbsp; Images

</button>


<button
    onclick="showMedia('video', this)">

🎥 &nbsp; Videos

</button>


</div>


<!-- STATS -->

<div class="stats">

<div class="stat">

<span>Posts</span>

<strong>{post_count}</strong>

</div>


<div class="stat">

<span>Images</span>

<strong>{image_count}</strong>

</div>


<div class="stat">

<span>Videos</span>

<strong>{video_count}</strong>

</div>

</div>


</aside>


<!-- ==========================================
     MAIN
     ========================================== -->

<main class="main">


<div class="page-header">

<h2 id="pageTitle">
Images
</h2>

<p id="pageDescription">
My photo collection
</p>

</div>


<div class="gallery" id="gallery">
"""


    # ==========================================
    # IMAGES
    # ==========================================

    for file in images:

        filename = file.name

        url_filename = quote(filename)


        html += f"""

<div class="card media-image">

<img
    src="media/{url_filename}"
    alt="Gallery Image"
    loading="lazy"
    decoding="async">

</div>

"""


    # ==========================================
    # VIDEOS
    # ==========================================

    for file in videos:

        filename = file.name

        url_filename = quote(filename)


        html += f"""

<div class="card media-video">

<video
    controls
    preload="none"
    playsinline>

<source
    src="media/{url_filename}">

Your browser does not support video.

</video>

</div>

"""


    # ==========================================
    # JAVASCRIPT
    # ==========================================

    html += """

</div>

</main>


<script>


function showMedia(type, button) {


    const cards =
        document.querySelectorAll(".card");


    // Remove active state

    document
        .querySelectorAll(".nav button")
        .forEach(btn => {

            btn.classList.remove("active");

        });


    // Activate clicked button

    button.classList.add("active");


    const title =
        document.getElementById("pageTitle");


    const description =
        document.getElementById("pageDescription");


    // ======================================
    // IMAGES
    // ======================================

    if (type === "image") {


        cards.forEach(card => {

            if (
                card.classList.contains(
                    "media-image"
                )
            ) {

                card.style.display = "block";

            }

            else {

                card.style.display = "none";

            }

        });


        title.innerText = "Images";

        description.innerText =
            "My photo collection";

    }


    // ======================================
    // VIDEOS
    // ======================================

    else if (type === "video") {


        cards.forEach(card => {

            if (
                card.classList.contains(
                    "media-video"
                )
            ) {

                card.style.display = "block";

            }

            else {

                card.style.display = "none";

            }

        });


        title.innerText = "Videos";

        description.innerText =
            "My video collection";

    }

}


</script>


</body>

</html>
"""


    # ==========================================
    # SAVE
    # ==========================================

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


    print(
        f"Website updated with {post_count} media files."
    )

    print(
        f"Images: {image_count} | "
        f"Videos: {video_count}"
    )


# ==========================================
# GIT PUSH
# ==========================================

def push_to_github():

    os.chdir(REPO_FOLDER)


    subprocess.run(
        ["git", "add", "."],
        check=True
    )


    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    )


    if result.returncode == 0:

        print("No changes to push.")

        return


    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "Update gallery"
        ],
        check=True
    )


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


# ==========================================
# START
# ==========================================

print()

print("======================================")

print("       CINE GALLERY AUTOMATION")

print("======================================")

print()

print("Media folder:")

print(MEDIA_FOLDER)

print()

print("Watching for new files...")

print("Press CTRL + C to stop.")

print()


# Initial update

create_website()

push_to_github()


# ==========================================
# WATCH
# ==========================================

while True:

    try:

        time.sleep(10)


        current_files = {

            file.name: (
                file.stat().st_size,
                file.stat().st_mtime
            )

            for file in Path(MEDIA_FOLDER).iterdir()

            if (
                file.is_file()
                and file.suffix.lower()
                in ALL_EXTENSIONS
            )

        }


        time.sleep(2)


        new_files = {

            file.name: (
                file.stat().st_size,
                file.stat().st_mtime
            )

            for file in Path(MEDIA_FOLDER).iterdir()

            if (
                file.is_file()
                and file.suffix.lower()
                in ALL_EXTENSIONS
            )

        }


        if current_files != new_files:

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