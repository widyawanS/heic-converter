import os
import json
import logging
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

import pillow_heif
from PIL import Image

# Get base directory (works from any location)
BASE_DIR = Path(__file__).parent.parent

# Setup logging
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_DIR / "error.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants - using dynamic paths based on BASE_DIR
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
CONVERTED_DIR = BASE_DIR / "data" / "converted"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_FORMATS = {"jpg", "png", "jpeg"}
ALLOWED_EXTENSIONS = {".heic"}
EXPIRY_HOURS = 24
METADATA_FILE = CONVERTED_DIR / "metadata.json"


def generate_file_id() -> str:
    """Generate unique file ID using UUID."""
    return str(uuid.uuid4())


def validate_heic_file(filename: str, file_content: bytes) -> Tuple[bool, Optional[str]]:
    """
    Validate if file is valid HEIC format.
    Returns: (is_valid, error_message)
    """
    # Check extension
    if not filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
        return False, f"File harus berformat HEIC. File yang diterima: {filename}"
    
    # Check magic bytes for HEIC/HEIF signature
    # HEIC files typically start with 'ftyp' or 'mdat'
    if len(file_content) < 12:
        return False, "File terlalu kecil atau bukan HEIC yang valid"
    
    # HEIF/HEIC files start with 'ftyp' (0x66747970)
    if not (file_content[4:8] == b'ftyp' or file_content[4:8] == b'mdat'):
        return False, "Magic bytes HEIC tidak ditemukan. File mungkin corrupt atau bukan HEIC"
    
    return True, None


def validate_format(format_str: str) -> Tuple[bool, Optional[str]]:
    """
    Validate output format.
    Returns: (is_valid, error_message)
    """
    if format_str.lower() not in ALLOWED_FORMATS:
        return False, f"Format harus salah satu dari: {', '.join(ALLOWED_FORMATS)}"
    return True, None


def validate_quality(quality: int) -> Tuple[bool, Optional[str]]:
    """
    Validate quality parameter.
    Returns: (is_valid, error_message)
    """
    if not isinstance(quality, int) or quality < 0 or quality > 100:
        return False, "Quality harus berupa integer antara 0-100"
    return True, None


def validate_dimensions(width: Optional[int], height: Optional[int]) -> Tuple[bool, Optional[str]]:
    """
    Validate width and height parameters.
    Returns: (is_valid, error_message)
    """
    if width is not None and (not isinstance(width, int) or width <= 0):
        return False, "Width harus berupa positive integer"
    
    if height is not None and (not isinstance(height, int) or height <= 0):
        return False, "Height harus berupa positive integer"
    
    return True, None


def convert_heic_to_image(
    input_path: str,
    output_path: str,
    format_str: str,
    quality: int = 85,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Convert HEIC to specified format with optional resize and quality settings.
    Returns: (success, error_message)
    """
    try:
        # Register HEIF opener for PIL
        pillow_heif.register_heif_opener()
        
        # Open HEIC file
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if needed for JPG/JPEG
            if format_str.lower() in ["jpg", "jpeg"] and img.mode in ["RGBA", "LA", "P"]:
                # Create white background
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode in ["RGBA", "LA"] else None)
                img = background
            
            # Resize if dimensions provided
            if width or height:
                if width and height:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                elif width:
                    ratio = width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                elif height:
                    ratio = height / img.height
                    new_width = int(img.width * ratio)
                    img = img.resize((new_width, height), Image.Resampling.LANCZOS)
            
            # Save with format and quality
            save_format = "JPEG" if format_str.lower() == "jpeg" else format_str.upper()
            if format_str.lower() in ["jpg", "jpeg"]:
                img.save(output_path, format=save_format, quality=quality, optimize=True)
            else:
                img.save(output_path, format=save_format, optimize=True)
        
        return True, None
    
    except Exception as e:
        error_msg = f"Konversi HEIC gagal: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


def save_metadata(file_id: str, original_filename: str, format_str: str, file_size: int) -> None:
    """Save file metadata for tracking and cleanup."""
    try:
        # Load existing metadata
        metadata_dict = {}
        if METADATA_FILE.exists():
            with open(METADATA_FILE, "r") as f:
                metadata_dict = json.load(f)
        
        # Calculate expiry time
        created_at = datetime.now().isoformat()
        expires_at = (datetime.now() + timedelta(hours=EXPIRY_HOURS)).isoformat()
        
        # Add new metadata
        metadata_dict[file_id] = {
            "original_filename": original_filename,
            "format": format_str,
            "file_size": file_size,
            "created_at": created_at,
            "expires_at": expires_at
        }
        
        # Save metadata
        with open(METADATA_FILE, "w") as f:
            json.dump(metadata_dict, f, indent=2)
    
    except Exception as e:
        logger.error(f"Gagal menyimpan metadata untuk {file_id}: {str(e)}")


def get_metadata(file_id: str) -> Optional[dict]:
    """Get metadata for a specific file ID."""
    try:
        if METADATA_FILE.exists():
            with open(METADATA_FILE, "r") as f:
                metadata_dict = json.load(f)
                return metadata_dict.get(file_id)
    except Exception as e:
        logger.error(f"Gagal membaca metadata untuk {file_id}: {str(e)}")
    
    return None


def delete_file_by_id(file_id: str) -> bool:
    """Delete converted file and its metadata."""
    try:
        # Find file (could be .jpg, .png, .jpeg)
        for ext in ["jpg", "png", "jpeg"]:
            file_path = CONVERTED_DIR / f"{file_id}.{ext}"
            if file_path.exists():
                file_path.unlink()
                
                # Remove from metadata
                if METADATA_FILE.exists():
                    with open(METADATA_FILE, "r") as f:
                        metadata_dict = json.load(f)
                    
                    if file_id in metadata_dict:
                        del metadata_dict[file_id]
                    
                    with open(METADATA_FILE, "w") as f:
                        json.dump(metadata_dict, f, indent=2)
                
                return True
        
        return False
    
    except Exception as e:
        logger.error(f"Gagal menghapus file {file_id}: {str(e)}")
        return False


def cleanup_expired_files() -> Tuple[int, int]:
    """
    Check and cleanup files older than EXPIRY_HOURS.
    Returns: (deleted_count, error_count)
    """
    deleted_count = 0
    error_count = 0
    
    try:
        if not METADATA_FILE.exists():
            return 0, 0
        
        with open(METADATA_FILE, "r") as f:
            metadata_dict = json.load(f)
        
        now = datetime.now()
        files_to_delete = []
        
        for file_id, metadata in metadata_dict.items():
            try:
                expires_at = datetime.fromisoformat(metadata["expires_at"])
                
                if now >= expires_at:
                    # File has expired, mark for deletion
                    if delete_file_by_id(file_id):
                        deleted_count += 1
                    else:
                        error_count += 1
            
            except Exception as e:
                logger.error(f"Error processing file {file_id} for cleanup: {str(e)}")
                error_count += 1
        
        if deleted_count > 0:
            logger.info(f"Cleanup selesai: {deleted_count} file dihapus, {error_count} error")
        
        return deleted_count, error_count
    
    except Exception as e:
        logger.error(f"Cleanup expired files error: {str(e)}")
        return 0, 1


def get_disk_space() -> dict:
    """Get disk space information."""
    try:
        import shutil
        disk_info = shutil.disk_usage("/home/sigitdev")
        return {
            "total": disk_info.total,
            "used": disk_info.used,
            "free": disk_info.free,
            "percent_used": (disk_info.used / disk_info.total) * 100
        }
    except Exception as e:
        logger.error(f"Error getting disk space: {str(e)}")
        return {}
