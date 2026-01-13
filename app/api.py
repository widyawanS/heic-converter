import logging
import shutil
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler

from utils import (
    generate_file_id,
    validate_heic_file,
    validate_format,
    validate_quality,
    validate_dimensions,
    convert_heic_to_image,
    save_metadata,
    get_metadata,
    delete_file_by_id,
    cleanup_expired_files,
    get_disk_space,
    CONVERTED_DIR,
)

# Setup logging - error logs only
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/sigitdev/logs/error.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Background scheduler for cleanup
scheduler = BackgroundScheduler()


def start_cleanup_scheduler():
    """Start background task to cleanup expired files every hour."""
    if not scheduler.running:
        scheduler.add_job(
            cleanup_expired_files,
            "interval",
            hours=1,
            id="cleanup_job",
            name="Cleanup expired files"
        )
        scheduler.start()
        logger.info("Cleanup scheduler started")


def shutdown_scheduler():
    """Shutdown scheduler on app shutdown."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Cleanup scheduler stopped")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle app startup and shutdown."""
    start_cleanup_scheduler()
    yield
    shutdown_scheduler()


# Initialize FastAPI app
app = FastAPI(
    title="HEIC to Image Converter API",
    description="API untuk konversi gambar HEIC menjadi JPG/PNG/JPEG dengan fitur resize dan quality control",
    version="1.0.0",
    lifespan=lifespan
)


@app.post("/convert")
async def convert_image(
    file: UploadFile = File(..., description="File HEIC yang akan dikonversi"),
    format: str = Form(..., description="Format output: jpg, png, atau jpeg"),
    quality: int = Form(85, description="Quality level 0-100 (default: 85)"),
    width: Optional[int] = Form(None, description="Target width (pixel), height akan auto-scale"),
    height: Optional[int] = Form(None, description="Target height (pixel), width akan auto-scale"),
    return_file: bool = Form(False, description="Return file langsung (True) atau JSON dengan URL (False)")
):
    """
    Konversi file HEIC ke format yang diinginkan.
    
    **Parameters:**
    - file: File HEIC yang akan dikonversi (required)
    - format: jpg, png, atau jpeg (required)
    - quality: Kualitas kompresi 0-100 (default: 85)
    - width: Lebar target dalam pixel (optional)
    - height: Tinggi target dalam pixel (optional)
    - return_file: Return file langsung atau JSON URL (default: False)
    
    **Response:**
    - Jika return_file=False: JSON dengan file_id, filename, url, expires_at
    - Jika return_file=True: File binary langsung
    """
    
    try:
        # ===== VALIDASI INPUT =====
        
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "code": "INVALID_FILENAME",
                    "message": "Filename tidak boleh kosong"
                }
            )
        
        # Validate format
        is_valid_format, format_error = validate_format(format)
        if not is_valid_format:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "code": "INVALID_FORMAT",
                    "message": format_error
                }
            )
        
        # Validate quality
        is_valid_quality, quality_error = validate_quality(quality)
        if not is_valid_quality:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "code": "INVALID_QUALITY",
                    "message": quality_error
                }
            )
        
        # Validate dimensions
        is_valid_dims, dims_error = validate_dimensions(width, height)
        if not is_valid_dims:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "code": "INVALID_DIMENSIONS",
                    "message": dims_error
                }
            )
        
        # ===== VALIDASI FILE =====
        
        # Read file content
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "code": "EMPTY_FILE",
                    "message": "File tidak boleh kosong"
                }
            )
        
        # Validate HEIC file
        is_valid_heic, heic_error = validate_heic_file(file.filename, file_content)
        if not is_valid_heic:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "code": "INVALID_HEIC",
                    "message": heic_error
                }
            )
        
        # ===== SETUP FILES =====
        
        # Generate unique IDs and paths
        file_id = generate_file_id()
        input_filename = file.filename
        output_filename = f"{Path(input_filename).stem}.{format.lower()}"
        
        # Create temporary input file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".heic") as tmp_input:
            tmp_input.write(file_content)
            tmp_input_path = tmp_input.name
        
        # Output path in converted directory
        output_path = CONVERTED_DIR / f"{file_id}.{format.lower()}"
        
        # ===== KONVERSI IMAGE =====
        
        success, conversion_error = convert_heic_to_image(
            input_path=tmp_input_path,
            output_path=str(output_path),
            format_str=format,
            quality=quality,
            width=width,
            height=height
        )
        
        # Cleanup temporary input file
        try:
            Path(tmp_input_path).unlink()
        except Exception as e:
            logger.error(f"Failed to delete temp file {tmp_input_path}: {str(e)}")
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "code": "CONVERSION_FAILED",
                    "message": conversion_error
                }
            )
        
        # ===== SAVE METADATA =====
        
        output_file_size = output_path.stat().st_size
        save_metadata(
            file_id=file_id,
            original_filename=output_filename,
            format_str=format,
            file_size=output_file_size
        )
        
        # ===== RETURN RESPONSE =====
        
        # Prepare response data
        response_data = {
            "status": "success",
            "file_id": file_id,
            "filename": output_filename,
            "size": output_file_size,
            "url": f"/download/{file_id}",
            "format": format.lower(),
            "quality": quality,
            "expires_at": (get_metadata(file_id) or {}).get("expires_at")
        }
        
        # Return file directly if requested
        if return_file:
            return FileResponse(
                path=str(output_path),
                filename=output_filename,
                media_type=f"image/{format if format != 'jpg' else 'jpeg'}"
            )
        
        # Otherwise return JSON response
        return response_data
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error during conversion: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Terjadi error saat memproses file",
                "details": str(e)
            }
        )


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Download file yang sudah dikonversi sebelumnya.
    
    **Parameters:**
    - file_id: ID file yang diterima dari response /convert endpoint
    
    **Response:**
    - File binary dengan Content-Disposition: attachment
    """
    
    try:
        # Get metadata
        metadata = get_metadata(file_id)
        
        if not metadata:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "code": "FILE_NOT_FOUND",
                    "message": f"File dengan ID {file_id} tidak ditemukan atau sudah expired"
                }
            )
        
        # Find the actual file (could be jpg, png, or jpeg)
        file_path = None
        for ext in ["jpg", "png", "jpeg"]:
            potential_path = CONVERTED_DIR / f"{file_id}.{ext}"
            if potential_path.exists():
                file_path = potential_path
                break
        
        if not file_path:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "code": "FILE_NOT_FOUND",
                    "message": f"File dengan ID {file_id} tidak ditemukan di storage"
                }
            )
        
        # Return file
        return FileResponse(
            path=str(file_path),
            filename=metadata.get("original_filename", "downloaded_image.jpg"),
            media_type=f"image/{file_path.suffix[1:]}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error downloading file {file_id}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "code": "DOWNLOAD_ERROR",
                "message": "Terjadi error saat mengunduh file",
                "details": str(e)
            }
        )


@app.delete("/delete/{file_id}")
async def delete_converted_file(file_id: str):
    """
    Delete file yang sudah dikonversi sebelumnya.
    
    **Parameters:**
    - file_id: ID file yang diterima dari response /convert endpoint
    
    **Response:**
    - JSON dengan status delete
    """
    
    try:
        # Get metadata to verify file exists
        metadata = get_metadata(file_id)
        
        if not metadata:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "code": "FILE_NOT_FOUND",
                    "message": f"File dengan ID {file_id} tidak ditemukan"
                }
            )
        
        # Delete file
        if delete_file_by_id(file_id):
            return {
                "status": "success",
                "message": f"File {file_id} berhasil dihapus",
                "file_id": file_id
            }
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "code": "DELETE_FAILED",
                    "message": "Gagal menghapus file"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error deleting file {file_id}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "code": "DELETE_ERROR",
                "message": "Terjadi error saat menghapus file",
                "details": str(e)
            }
        )


@app.get("/health")
async def health_check():
    """
    Check API health status dan disk space.
    
    **Response:**
    - JSON dengan status, uptime, disk space, dan scheduler info
    """
    
    try:
        disk_info = get_disk_space()
        
        return {
            "status": "healthy",
            "api_version": "1.0.0",
            "scheduler_running": scheduler.running,
            "disk": {
                "total_gb": round(disk_info.get("total", 0) / (1024**3), 2),
                "used_gb": round(disk_info.get("used", 0) / (1024**3), 2),
                "free_gb": round(disk_info.get("free", 0) / (1024**3), 2),
                "percent_used": round(disk_info.get("percent_used", 0), 2)
            }
        }
    
    except Exception as e:
        error_msg = f"Health check error: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "degraded",
            "message": "Beberapa komponen sedang bermasalah",
            "error": str(e)
        }


@app.get("/")
async def root():
    """Root endpoint - API info."""
    return {
        "name": "HEIC to Image Converter API",
        "version": "1.0.0",
        "description": "API untuk konversi gambar HEIC menjadi JPG/PNG/JPEG",
        "endpoints": {
            "POST /convert": "Konversi file HEIC ke format lain",
            "GET /download/{file_id}": "Download file yang sudah dikonversi",
            "DELETE /delete/{file_id}": "Hapus file yang sudah dikonversi",
            "GET /health": "Check status API",
            "GET /docs": "Interactive API documentation (Swagger UI)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
