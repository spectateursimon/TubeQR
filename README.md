![Header](./header.png)

# TubeQR

Generate QR codes for all videos in a YouTube playlist - perfect for educational materials, advent calendars or sharing playlists!

## Features

- 🎬 Works with YouTube playlists and single videos
- 🚫 No video downloads - fetches metadata only
- 🔢 Numbered output: `01_VideoTitle.png`, `02_VideoTitle.png`, etc.
- 📋 Creates an overview text file with all video links
- ⚡ Fast and lightweight

## Installation

```bash
# Clone the repository
git clone https://github.com/spectateursimon/TubeQR.git
cd TubeQR

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python3 tubeqr.py
```

Then enter your YouTube playlist or video URL when prompted.

### Example

```
TubeQR - YouTube Playlist QR Code Generator
============================================================

Please enter the YouTube link: https://www.youtube.com/playlist?list=...

📋 Fetching playlist information...
✅ 26 video(s) found

🔄 Generating QR codes...
  ✅ [01/26] 01_First_Video.png
  ✅ [02/26] 02_Second_Video.png
  ...
  ✅ [26/26] 26_Last_Video.png

✅ All QR codes have been successfully created!
```

## Output Structure

```
youtube_qr_codes/
└── playlist_YYYYMMDD_HHMMSS/
    ├── overview.txt          # List of all videos and URLs
    └── qr_codes/             # PNG files
        ├── 01_VideoTitle.png
        ├── 02_VideoTitle.png
        └── ...
```

## Requirements

- Python 3.7+
- `qrcode[pil]` - QR code generation
- `yt-dlp` - YouTube metadata extraction

## Use Cases

- 📅 **Advent Calendars**: Print QR codes for daily video reveals
- 🎓 **Education**: Create scannable links for course playlists
- 🎁 **Gifts**: Share playlists in a physical format
- 📱 **Easy Sharing**: Convert playlists to scannable codes

## License

MIT License - feel free to use and modify!

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
