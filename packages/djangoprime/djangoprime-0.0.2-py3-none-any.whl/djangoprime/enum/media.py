from djangoprime.core.base import BaseEnum


class AudioExceptionEnum(BaseEnum):
    MISSING_AUDIO_KEY = 'Missing "audio" key'
    WRONG_AUDIO_TYPE = 'Invalid audio type. Please upload a supported format.'
    AUDIO_TOO_LARGE = 'Audio file size exceeds the allowed limit.'
    UNSUPPORTED_AUDIO_FORMAT = 'Unsupported audio format.'
    AUDIO_PROCESSING_ERROR = 'Error processing the audio file.'
    AUDIO_PLAYBACK_ERROR = 'Error playing the audio file.'
    AUDIO_NOT_FOUND = 'Audio file not found.'
    AUDIO_CORRUPTED = 'Audio file appears to be corrupted.'
    INSUFFICIENT_STORAGE = 'Insufficient storage space to upload the audio file.'
    AUDIO_UPLOAD_TIMEOUT = 'Audio file upload timed out.'
    AUDIO_DELETION_FAILED = 'Audio file deletion failed.'
    AUDIO_ALREADY_EXISTS = 'A audio file with the same name already exists.'


class FileExceptionEnum(BaseEnum):
    MISSING_FILE_KEY = 'Missing "file" key'
    WRONG_FILE_TYPE = 'Invalid file type. Please upload a supported format.'
    FILE_TOO_LARGE = 'File size exceeds the allowed limit.'
    FILE_NOT_FOUND = 'File not found.'
    PERMISSION_DENIED = 'Permission denied for the requested file operation.'
    FILE_READ_ERROR = 'Error reading the file.'
    FILE_WRITE_ERROR = 'Error writing to the file.'
    FILE_CORRUPTED = 'The file appears to be corrupted.'
    INSUFFICIENT_STORAGE = 'Insufficient storage space to upload the file.'
    FILE_UPLOAD_TIMEOUT = 'File upload timed out. Please try again.'
    FILE_DELETION_FAILED = 'Failed to delete the file.'
    FILE_ALREADY_EXISTS = 'A file with the same name already exists.'


class ImageExceptionEnum(BaseEnum):
    MISSING_IMAGE_KEY = 'Missing "image" key'
    WRONG_IMAGE_TYPE = 'Invalid image type. Please upload a supported format.'
    IMAGE_TOO_LARGE = 'Image size exceeds the allowed limit.'
    UNSUPPORTED_IMAGE_FORMAT = 'Unsupported image format.'
    IMAGE_RESOLUTION_TOO_HIGH = 'Image resolution exceeds the maximum allowed size.'
    IMAGE_PROCESSING_ERROR = 'Error processing the image.'
    IMAGE_NOT_FOUND = 'Image not found.'
    IMAGE_CORRUPTED = 'The image appears to be corrupted.'
    IMAGE_UPLOAD_TIMEOUT = 'Image upload timed out. Please try again.'
    IMAGE_DELETION_FAILED = 'Failed to delete image'
    IMAGE_ALREADY_EXISTS = 'A image with the same name already exists.'
    INSUFFICIENT_STORAGE = 'Insufficient storage space to upload the image file.'


class VideoExceptionEnum(BaseEnum):
    MISSING_VIDEO_KEY = 'Missing "video" key'
    WRONG_VIDEO_TYPE = 'Invalid video type. Please upload a supported format.'
    VIDEO_TOO_LARGE = 'Video file size exceeds the allowed limit.'
    UNSUPPORTED_VIDEO_FORMAT = 'Unsupported video format.'
    VIDEO_PROCESSING_ERROR = 'Error processing the video file.'
    VIDEO_PLAYBACK_ERROR = 'Error playing the video file.'
    VIDEO_ENCODING_ERROR = 'Error encoding the video file.'
    VIDEO_NOT_FOUND = 'Video not found.'
    VIDEO_CORRUPTED = 'The video  appears to be corrupted.'
    INSUFFICIENT_STORAGE = 'Insufficient storage space to upload the video file.'
    VIDEO_UPLOAD_TIMEOUT = 'Video upload timed out. Please try again.'
    VIDEO_DELETION_FAILED = 'Failed to delete the video.'
    VIDEO_ALREADY_EXISTS = 'A video with the same name already exists.'
