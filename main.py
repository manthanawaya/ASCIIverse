import os
import sys
import time
import glob
import cv2
import numpy as np
import yt_dlp

ASCII_PALETTE = " .:-=+*#%@"


# -------------------------------------------------------------
# 1. FETCH VIDEO BY DESCRIPTION (Zero APIs, 100% Free)
# -------------------------------------------------------------
def fetch_video_by_prompt(prompt: str) -> str:
    print(f"\n[1/2] Searching and retrieving video for: '{prompt}'...")

    # Clean old downloaded clips
    for old_file in glob.glob("temp_clip.*"):
        try:
            os.remove(old_file)
        except OSError:
            pass

    # Search and fetch a short, lightweight clip matching your words
    ydl_opts = {
        "format": "bestvideo[height<=360][ext=mp4]/best[height<=360]",
        "outtmpl": "temp_clip.%(ext)s",
        "default_search": "ytsearch1",
        "quiet": True,
        "no_warnings": True,
    }

    search_query = f"{prompt} short clip"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    # Find the downloaded file
    matching = glob.glob("temp_clip.*")
    if not matching:
        print("\nError: Could not retrieve a video matching your prompt.")
        sys.exit(1)

    print("[1/2] Video ready!")
    return matching[0]


# -------------------------------------------------------------
# 2. FRAME TO ASCII CONVERTER
# -------------------------------------------------------------
def frame_to_ascii(frame: np.ndarray, width: int = 80) -> str:
    h, w = frame.shape[:2]
    height = int(width * (h / w) * 0.55)

    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    palette_len = len(ASCII_PALETTE)
    indices = (gray / 255.0 * (palette_len - 1)).astype(int)

    lines = ["".join(ASCII_PALETTE[val] for val in row) for row in indices]
    return "\n".join(lines)


# -------------------------------------------------------------
# 3. TERMINAL ASCII PLAYER
# -------------------------------------------------------------
def play_ascii(video_path: str, width: int = 80):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    frame_delay = 1.0 / fps

    print("\n[2/2] Starting ASCII Playback! (Press Ctrl+C to stop)")
    time.sleep(1)

    os.system("cls" if os.name == "nt" else "clear")

    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            sys.stdout.write("\033[H" + frame_to_ascii(frame, width=width))
            sys.stdout.flush()

            elapsed = time.time() - start_time
            sleep_time = max(0.0, frame_delay - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\n\nPlayback complete.")


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":
    prompt = input("Describe what you want to see: ").strip()
    if not prompt:
        prompt = "campfire in the woods"

    video_file = fetch_video_by_prompt(prompt)
    play_ascii(video_file, width=90)