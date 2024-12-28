import requests
from loguru import logger


def download_from_s3(presigned_url, f):
    response = requests.get(presigned_url)
    response.raise_for_status()

    logger.debug("Downloaded object from S3")
    f.write(response.content)
    f.seek(0)


def delete_s3_obj(presigned_delete_url, raises=True):
    r = requests.delete(presigned_delete_url)
    if raises:
        r.raise_for_status()
    logger.debug("Deleted object from S3")
