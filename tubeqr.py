#!/usr/bin/env python3
"""
TubeQR - YouTube Playlist QR Code Generator

This program:
1. Asks for a YouTube playlist link
2. Extracts all video information (without downloading!)
3. Generates a QR code for each video
4. Saves QR codes as PNG files with format: 01_VideoTitle.png
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime

try:
    import qrcode
except ImportError:
    print("❌ qrcode is not installed.")
    print("Install it with: pip install qrcode[pil]")
    sys.exit(1)


def ensure_dir(path: Path) -> Path:
    """Creates directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_youtube_link():
    """Asks the user for a YouTube link (playlist or video)"""
    print("\n" + "="*60)
    print("TubeQR - YouTube Playlist QR Code Generator")
    print("="*60)

    while True:
        link = input("\nPlease enter the YouTube link (playlist or single video): ").strip()

        # Simple validation
        if "youtube.com" in link or "youtu.be" in link:
            return link
        else:
            print("⚠️  This doesn't seem to be a valid YouTube link.")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                sys.exit(0)


def sanitize_filename(filename: str) -> str:
    """Removes invalid characters from filenames"""
    # Replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Shorten too long names
    if len(filename) > 100:
        filename = filename[:100]
    return filename.strip()


def get_playlist_info(url: str) -> list:
    """Extracts playlist information with yt-dlp (without downloading videos)"""
    print(f"\n📋 Fetching playlist information...")

    try:
        # Check if yt-dlp is installed
        subprocess.run(["yt-dlp", "--version"],
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  yt-dlp is not installed.")
        print("Install it with: pip install yt-dlp")
        sys.exit(1)

    # Extract only metadata, no downloads
    cmd = [
        "yt-dlp",
        "--flat-playlist",  # Don't download videos
        "--dump-json",      # JSON output
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Parse JSON for each video
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                video_data = json.loads(line)
                videos.append(video_data)

        print(f"✅ {len(videos)} video(s) found")
        return videos

    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching playlist information: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing video data: {e}")
        sys.exit(1)


def generate_qr_code(url: str, output_path: Path, size: int = 10):
    """Generates a QR code and saves it as PNG"""
    # Create QR code
    qr = qrcode.QRCode(
        version=1,  # Automatic size
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save as PNG
    img.save(str(output_path))


def main():
    """Main function"""
    # Create main output folder with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_output_dir = ensure_dir(Path.cwd() / "youtube_qr_codes")
    output_dir = ensure_dir(base_output_dir / f"playlist_{timestamp}")

    print(f"\n📁 Output folder created: {output_dir}")

    # Get YouTube link
    youtube_url = get_youtube_link()

    # Get playlist information
    videos = get_playlist_info(youtube_url)

    if not videos:
        print("\n⚠️  No videos found.")
        return

    # Generate QR codes
    print(f"\n🔄 Generating QR codes...")

    # Create subfolder for QR codes
    qr_dir = ensure_dir(output_dir / "qr_codes")

    # Also create an overview file
    overview_path = output_dir / "overview.txt"

    with open(overview_path, 'w', encoding='utf-8') as overview_file:
        overview_file.write(f"YouTube Playlist QR Codes\n")
        overview_file.write(f"{'='*60}\n")
        overview_file.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        overview_file.write(f"Number of videos: {len(videos)}\n\n")

        for idx, video in enumerate(videos, 1):
            # Extract video information
            video_id = video.get('id', 'unknown')
            video_title = video.get('title', f'Video {idx}')
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Sanitize filename
            safe_title = sanitize_filename(video_title)

            # Create filename with numbering
            qr_filename = f"{idx:02d}_{safe_title}.png"
            qr_path = qr_dir / qr_filename

            # Generate QR code
            try:
                generate_qr_code(video_url, qr_path)
                print(f"  ✅ [{idx:02d}/{len(videos)}] {qr_filename}")

                # Write to overview
                overview_file.write(f"{idx:02d}. {video_title}\n")
                overview_file.write(f"    URL: {video_url}\n")
                overview_file.write(f"    QR Code: {qr_filename}\n\n")

            except Exception as e:
                print(f"  ❌ [{idx:02d}/{len(videos)}] Error with {video_title}: {e}")
                overview_file.write(f"{idx:02d}. {video_title}\n")
                overview_file.write(f"    ERROR: {e}\n\n")

    print(f"\n✅ All QR codes have been successfully created!")
    print(f"\n📁 Output:")
    print(f"   - QR Codes: {qr_dir}")
    print(f"   - Overview: {overview_path}")

    print("\n" + "="*60)
    print("✨ Program completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program aborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
