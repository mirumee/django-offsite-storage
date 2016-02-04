# django-offsite-storage
Cloud static and media file storage suitable for app containers


## Installation

Install the package via `pip`:

    pip install django-offsite-storage
  
  
Then add `'offsite_storage'` to your `INSTALLED_APPS` just before `'django.contrib.staticfiles'`.

`django-offsite-storage` overrides default `collectstatic` command to exclude unnecessary files (`less`, `scss`) from the process.

## Amazon S3
  
Set following settings in your project's settings:

 * AWS_ACCESS_KEY_ID
 * AWS_SECRET_ACCESS_KEY
 * AWS_STATIC_BUCKET_NAME
 * STATICFILES_STORAGE = 'offsite_storage.storages.CachedS3FilesStorage'

If you intend to use an external storage for your `media files`, set the following settings:

 * AWS_MEDIA_BUCKET_NAME
 * DEFAULT_FILE_STORAGE = 'offsite_storage.storages.S3MediaStorage'
 * THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

In the case when you use a different s3 account for your media files, set the following settings:

 * AWS_MEDIA_ACCESS_KEY_ID
 * AWS_MEDIA_SECRET_ACCESS_KEY

To force boto to use a particular S3 host set AWS_S3_ENDPOINT (default is `s3.amazonaws.com`).
