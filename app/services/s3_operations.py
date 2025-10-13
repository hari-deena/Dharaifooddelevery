from typing import List
from fastapi import UploadFile
from app.core.s3_config import s3_client, bucket_name
from app.core.logger_config import configure_logger

logger = configure_logger("s3_operations")

async def upload_images_to_s3(images: List[UploadFile], folder: str):
    try:
        uploaded_urls = []

        for image in images:
            image_data = await image.read()  # Read image content in memory
            file_key = f"{folder}/{image.filename}"

            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=image_data,
                ContentType=image.content_type,
                ACL='public-read'
            )

            logger.info(f"Uploaded file {file_key}")
            uploaded_urls.append(file_key)

        return uploaded_urls

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return None

def get_presigned_url(image_key):
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': image_key},
            ExpiresIn=604800  # 7 days in seconds
        )
        logger.info(f"Generated presigned URL for {image_key}")
        return url
    except Exception as e:
        logger.error(f"Error generating presigned URL for {image_key}: {e}")
        return None
    


from typing import List, Optional

def delete_s3_folder_objects(prefix: str) -> Optional[List[str]]:
    deleted_keys = []
    continuation_token = None

    try:
        while True:
            list_kwargs = {'Bucket': bucket_name, 'Prefix': prefix}
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token

            response = s3_client.list_objects_v2(**list_kwargs)
            contents = response.get('Contents', [])

            if not contents:
                # No objects found in the folder
                break

            objects_to_delete = [{'Key': obj['Key']} for obj in contents]
            delete_response = s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={'Objects': objects_to_delete}
            )

            deleted = [obj['Key'] for obj in delete_response.get('Deleted', [])]
            errors = delete_response.get('Errors', [])

            if errors:
                logger.error(f"Failed to delete some objects: {errors}")
                return None

            deleted_keys.extend(deleted)

            if response.get('IsTruncated'):
                continuation_token = response.get('NextContinuationToken')
            else:
                break

        if not deleted_keys:
            # If no keys were deleted
            return None

        logger.info(f"Successfully deleted keys: {deleted_keys}")
        return deleted_keys

    except Exception as e:
        logger.error(f"Exception during deletion: {e}")
        return None

# Usage
# deleted_images = delete_s3_folder_objects(folder)
# if deleted_images is None:
#     print("No objects found or deleted in the folder.")
# else:
#     print(f"Deleted objects: {deleted_images}")
