#!/usr/bin/env python3

import os
import sqlite3
import hashlib
import subprocess
import io
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        name TEXT PRIMARY KEY,
        digest TEXT,
        size INT,
        width INT,
        height INT,
        mtime INT,
        data BLOB
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS previews (
        name TEXT,
        width INT,
        height INT,
        data BLOB
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_previews_name ON previews(name)")

    return conn, cursor


def get_file_digest(file_path):
    """Calculate SHA-256 hash of file"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_image_dimensions(file_path):
    """Get image dimensions using ImageMagick identify"""
    try:
        result = subprocess.run(
            ["identify", "-format", "%w %h", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        width, height = map(int, result.stdout.strip().split())
        return width, height
    except subprocess.CalledProcessError as e:
        print(f"Error getting dimensions for {file_path}: {e}")
        return None, None


def convert_image(file_path, convert_format):
    """Convert image to specified format"""
    try:
        format_name, quality = (
            convert_format.split(":")
            if ":" in convert_format
            else (convert_format, None)
        )
        convert_cmd = ["convert", file_path, "-strip"]

        if quality:
            if format_name.lower() == "webp":
                convert_cmd.extend(["-quality", quality])
            elif format_name.lower() in ("jpg", "jpeg"):
                convert_cmd.extend(["-quality", quality])
            elif format_name.lower() == "png":
                convert_cmd.extend(["-quality", quality])

        convert_cmd.append(f"{format_name.upper()}:-")

        result = subprocess.run(convert_cmd, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error converting image {file_path}: {e}")
        return None


def create_preview(file_path, max_size=200):
    """Create preview using ImageMagick convert"""
    try:
        # Generate random filename for preview
        preview_filename = hashlib.md5(os.urandom(16)).hexdigest() + ".webp"
        preview_path = os.path.join("/tmp", preview_filename)

        # Create preview maintaining aspect ratio
        subprocess.run(
            [
                "convert",
                file_path,
                "-resize",
                f"{max_size}x{max_size}>",  # > means only shrink larger images
                "-strip",  # Remove metadata
                "-quality",
                "80",
                f"WEBP:{preview_path}",
            ],  # Output WEBP to temp file
            check=True,
        )

        # Get preview dimensions
        dims = subprocess.run(
            ["identify", "-format", "%w %h", preview_path],
            capture_output=True,
            text=True,
            check=True,
        )

        # Read preview data
        with open(preview_path, "rb") as f:
            preview_data = f.read()

        os.remove(preview_path)

        preview_width, preview_height = map(int, dims.stdout.strip().split())
        return preview_data, preview_width, preview_height

    except subprocess.CalledProcessError as e:
        print(f"Error creating preview for {file_path}: {e}")
        return None, None, None


def strip_extension(filename):
    """Remove file extension from filename"""
    return os.path.splitext(filename)[0]


def process_single_image(args):
    """Process a single image file"""
    img_file, convert_format, db_path = args

    # Create new connection for this thread
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        file_path = os.path.join(".", img_file)
        mtime = int(os.path.getmtime(file_path))

        # Strip extension from filename if converting
        db_filename = strip_extension(img_file) if convert_format else img_file

        # Get dimensions using ImageMagick
        width, height = get_image_dimensions(file_path)
        if width is None:
            return

        # Convert image if format specified
        if convert_format:
            img_data = convert_image(file_path, convert_format)
            if img_data is None:
                return
        else:
            with open(file_path, "rb") as f:
                img_data = f.read()

        # Get size and digest of the processed image data
        file_size = len(img_data)
        digest = hashlib.sha256(img_data).hexdigest()

        # Create preview
        preview_data, preview_width, preview_height = create_preview(file_path)
        if preview_data is None:
            return

        # Insert into images table
        cursor.execute(
            """
        INSERT OR REPLACE INTO images
        (name, digest, size, width, height, mtime, data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (db_filename, digest, file_size, width, height, mtime, img_data),
        )

        # Insert into previews table
        cursor.execute(
            """
        INSERT OR REPLACE INTO previews
        (name, width, height, data)
        VALUES (?, ?, ?, ?)
        """,
            (db_filename, preview_width, preview_height, preview_data),
        )

        conn.commit()
        conn.close()
        return f"Processed {img_file}"

    except Exception as e:
        if conn:
            conn.close()
        return f"Error processing {img_file}: {str(e)}"


def process_images(convert_format=None, num_threads=1, output_path="output.imglite"):
    # Initialize database
    conn, cursor = create_database(output_path)
    conn.close()

    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff")
    image_files = [f for f in os.listdir(".") if f.lower().endswith(image_extensions)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        args = [(img_file, convert_format, output_path) for img_file in image_files]

        # Process files with progress bar
        for result in tqdm(
            executor.map(process_single_image, args),
            total=len(image_files),
            desc="Processing images",
        ):
            if result:
                pass


def cli():
    parser = argparse.ArgumentParser(description="Process images into SQLite database")
    parser.add_argument(
        "--convert",
        help="Convert images to specified format (e.g., webp:80 for WebP at 80% quality)",
        default=None,
    )
    parser.add_argument(
        "-j", "--jobs", help="Number of parallel jobs", type=int, default=1
    )
    parser.add_argument(
        "--output", help="Output database path/filename", default="output.imglite"
    )
    args = parser.parse_args()

    process_images(args.convert, args.jobs, args.output)
