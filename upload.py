import os
import time
import subprocess
from pathlib import Path
from urllib.parse import quote


# ==========================================
# YOUR PATHS
# ==========================================

REPO_FOLDER = r"C:\Users\Mahith Chowdary\Downloads\cine-gallery"

MEDIA_FOLDER = r"C:\Users\Mahith Chowdary\Downloads\cine-gallery\media"


# ==========================================
# SUPPORTED FILE TYPES
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

        if file.is_file() and file.suffix.lower() in ALL_EXTENSIONS:
            files.append(file)

    # Sort files alphabetically
    files.sort(key=lambda x: x.name.lower())

    # Count images and videos
    image_count = sum(
        1 for file in files
        if file.suffix.lower() in IMAGE_EXTENSIONS
    )

    video_count = sum(
        1 for file in files
        if file.suffix.lower() in VIDEO_EXTENSIONS
    )

    post_count = len(files)


    # ==========================================
    # WEBSITE HTML
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


* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}


body {{

    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            135deg,
            #0f0f0f,
            #1b1b1b
        );

    color: white;

    min-height: 100vh;

}}


/* ==========================================
   HEADER
   ========================================== */

header {{

    text-align: center;

    padding: 60px 20px 40px;

}}


header h1 {{

    font-size: 48px;

    letter-spacing: 2px;

    margin-bottom: 12px;

}}


header p {{

    color: #999;

    font-size: 17px;

}}


/* ==========================================
   POST COUNT
   ========================================== */

.stats {{

    display: flex;

    justify-content: center;

    gap: 12px;

    flex-wrap: wrap;

    margin-top: 20px;

}}


.stat {{

    display: inline-block;

    padding: 9px 18px;

    border-radius: 30px;

    background: #222;

    color: #aaa;

    font-size: 14px;

}}


.stat strong {{

    color: white;

    font-size: 16px;

}}


/* ==========================================
   GALLERY
   ========================================== */

.gallery {{

    width: 92%;

    max-width: 1400px;

    margin: auto;

    display: grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(280px, 1fr)
        );

    gap: 25px;

    padding-bottom: 60px;

}}


/* ==========================================
   CARD
   ========================================== */

.card {{

    background: #191919;

    border-radius: 18px;

    padding: 10px;

    overflow: hidden;

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;

}}


.card:hover {{

    transform: translateY(-8px);

    box-shadow:
        0 20px 50px
        rgba(0, 0, 0, 0.6);

}}


/* ==========================================
   IMAGE / VIDEO
   ========================================== */

.card img,
.card video {{

    width: 100%;

    height: 380px;

    object-fit: cover;

    border-radius: 12px;

    display: block;

}}


/* ==========================================
   FOOTER
   ========================================== */

footer {{

    text-align: center;

    padding: 30px;

    color: #666;

}}


/* ==========================================
   MOBILE
   ========================================== */

@media (max-width: 600px) {{

    header h1 {{

        font-size: 34px;

    }}

    .gallery {{

        width: 94%;

        grid-template-columns: 1fr;

    }}

    .card img,
    .card video {{

        height: auto;

    }}

}}


</style>

</head>


<body>


<!-- ==========================================
     HEADER
     ========================================== -->

<header>

<h1>🎬 Cine Gallery</h1>

<p>My collection of photos and videos</p>


<div class="stats">

    <div class="stat">
        <strong>{post_count}</strong> Posts
    </div>

    <div class="stat">
        <strong>{image_count}</strong> Photos
    </div>

    <div class="stat">
        <strong>{video_count}</strong> Videos
    </div>

</div>


</header>


<!-- ==========================================
     GALLERY
     ========================================== -->

<main class="gallery">
"""


    # ==========================================
    # ADD ALL MEDIA AUTOMATICALLY
    # ==========================================

    for file in files:

        filename = file.name

        # Safely encode filename for website URL
        url_filename = quote(filename)

        extension = file.suffix.lower()


        # ======================================
        # IMAGE
        # ======================================

        if extension in IMAGE_EXTENSIONS:

            html += f"""

<div class="card">

<img
    src="media/{url_filename}"
    alt="Gallery Image"
    loading="lazy">

</div>

"""


        # ======================================
        # VIDEO
        # ======================================

        elif extension in VIDEO_EXTENSIONS:

            html += f"""

<div class="card">

<video
    controls
    preload="metadata">

<source
    src="media/{url_filename}">

Your browser does not support video.

</video>

</div>

"""


    # ==========================================
    # CLOSE HTML
    # ==========================================

    html += """

</main>


<footer>

© 2026 Cine Gallery

</footer>


</body>

</html>
"""


    # ==========================================
    # SAVE INDEX.HTML
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
        f"Photos: {image_count} | Videos: {video_count}"
    )


# ==========================================
# GIT PUSH
# ==========================================

def push_to_github():

    os.chdir(REPO_FOLDER)


    # ======================================
    # ADD CHANGES
    # ======================================

    subprocess.run(
        ["git", "add", "."],
        check=True
    )


    # ======================================
    # CHECK FOR CHANGES
    # ======================================

    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    )


    # No changes
    if result.returncode == 0:

        print("No changes to push.")

        return


    # ======================================
    # COMMIT
    # ======================================

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "Update gallery"
        ],
        check=True
    )


    # ======================================
    # PUSH TO GITHUB
    # ======================================

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
# MAIN AUTOMATION
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


# ==========================================
# FIRST UPDATE
# ==========================================

create_website()

push_to_github()


# ==========================================
# KEEP WATCHING
# ==========================================

while True:

    try:

        # Check every 10 seconds
        time.sleep(10)


        # Get current state of media folder

        current_files = {

            file.name: (
                file.stat().st_size,
                file.stat().st_mtime
            )

            for file in Path(MEDIA_FOLDER).iterdir()

            if (
                file.is_file()
                and file.suffix.lower() in ALL_EXTENSIONS
            )

        }


        # Wait a little

        time.sleep(2)


        # Get new state

        new_files = {

            file.name: (
                file.stat().st_size,
                file.stat().st_mtime
            )

            for file in Path(MEDIA_FOLDER).iterdir()

            if (
                file.is_file()
                and file.suffix.lower() in ALL_EXTENSIONS
            )

        }


        # ======================================
        # DETECT NEW/CHANGED MEDIA
        # ======================================

        if current_files != new_files:

            print()

            print("📸 New media detected!")

            print()


            # Update website

            create_website()


            # Push to GitHub

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

        print("Trying again in 10 seconds...")

        time.sleep(10)