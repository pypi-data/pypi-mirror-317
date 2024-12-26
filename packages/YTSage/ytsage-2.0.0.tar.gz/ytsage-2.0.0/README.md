# YTSage

YTSage is a graphical user interface (GUI) for the popular command-line tool `yt-dlp`, which is used for downloading videos from YouTube and other video platforms. YTSage provides an easy-to-use interface for downloading videos, selecting formats, and managing downloads.

## Features

*   **Analyze URLs:** Quickly analyze YouTube URLs (both videos and playlists).
*   **Format Selection:** Choose from available video and audio formats.
*   **Subtitle Support:** Download subtitles in various languages (if available).
*   **Download Management:** Pause, resume, and cancel downloads.
*   **Custom Commands:** Run custom `yt-dlp` commands.
*   **Progress Tracking:** Monitor download progress with a progress bar and status updates.
*   **FFmpeg Integration:** Automatically merges audio and video if needed (requires FFmpeg to be installed).
*   **Dark Mode Theme:** A modern, dark-themed interface.

## Installation

### Prerequisites
* FFmpeg is required to be installed separately. You can find instructions on how to install FFmpeg [here](https://github.com/oop7/ffmpeg-install-guide).

### From PyPI
YTSage can be installed via pip:
```bash
pip install YTSage
```

- This will also install the required dependencies (yt-dlp, PyQt6, requests, Pillow, packaging)

## Usage

After installation, you can run YTSage from your terminal:

```bash
YTSage
```

1. Paste a YouTube URL into the URL input field.
2. Click **Analyze** to analyze the URL.
3. Select the desired video/audio format from the table.
4. Choose a download location (optional).
5. Click **Download** to start the download.


## Contributing

Contributions are welcome! If you find a bug or want to suggest a new feature, please open an issue or submit a pull request on the [GitHub repository](https://github.com/oop7/YTSage).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
