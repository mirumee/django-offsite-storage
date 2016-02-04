from django.conf import settings


AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
AWS_STATIC_BUCKET_NAME = getattr(settings, 'AWS_STATIC_BUCKET_NAME')

AWS_MEDIA_ACCESS_KEY_ID = getattr(
    settings, 'AWS_MEDIA_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID)
AWS_MEDIA_SECRET_ACCESS_KEY = getattr(
    settings, 'AWS_MEDIA_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY)
AWS_MEDIA_BUCKET_NAME = getattr(settings, 'AWS_MEDIA_BUCKET_NAME')

AWS_S3_ENDPOINT = getattr(
    settings, 'AWS_S3_ENDPOINT', 's3.amazonaws.com')
AWS_HOST_URL = 'https://%%(bucket_name)s.%s/' % AWS_S3_ENDPOINT
AWS_POLICY = 'public-read'

IGNORE_FILES = getattr(settings, 'OFFSITE_STORAGE_IGNORE_FILES',
                       ['*.less', '*.scss', '*.txt', 'components'])
