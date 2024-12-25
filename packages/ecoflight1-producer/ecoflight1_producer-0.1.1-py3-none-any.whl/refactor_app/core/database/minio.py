import minio
from refactor_app.core.config import settings


def get_minio_client():
    return minio.Minio(
            endpoint=settings.minio.ENDPOINT,
            access_key=settings.minio.ACCESS_KEY,
            secret_key=settings.minio.SECRET_KEY,
            secure=False
        )