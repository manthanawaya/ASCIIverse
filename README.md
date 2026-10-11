# ASCIIverse

ASCIIverse is a lightweight Python project that turns a text prompt into a terminal-based ASCII art playback experience. It searches for a short video matching your description, downloads it locally, and renders it frame-by-frame in your terminal using a custom ASCII palette.

## Features

- Prompt-driven video lookup with YouTube search
- Automatic short-video download using `yt-dlp`
- Real-time ASCII conversion from video frames
- Terminal playback with smooth frame timing
- No API key required

## How it works

1. You enter a prompt such as `forest at sunset` or `cyberpunk city night`.
2. The script searches YouTube for a matching short clip.
3. It downloads the clip to a temporary file.
4. Each frame is resized, converted to grayscale, and mapped to ASCII characters.
5. The video plays in your terminal as animated ASCII art.

## Project structure

- `main.py` — main application logic
- `.gitignore` — ignores generated temporary media files

## Requirements

- Python 3.9+
- OpenCV (`cv2`)
- NumPy
- `yt-dlp`

Install dependencies:

```bash
pip install numpy opencv-python yt-dlp
```

## Usage

From the project root, run:

```bash
python main.py
```

Then enter a description when prompted, for example:

```text
Describe what you want to see: dragon flying over mountains
```

The script will fetch a matching short clip and begin ASCII playback in the terminal.

## Notes

- The project relies on a public YouTube search and may vary depending on availability and network conditions.
- Video playback is intentionally lightweight and designed for terminal-based viewing.
- Temporary clip files are cleaned up before each new search.

## License

This project is provided as-is for personal and educational use.
