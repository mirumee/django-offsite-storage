from __future__ import unicode_literals
from collections import OrderedDict
import logging
import mimetypes
from tempfile import TemporaryFile

from boto.s3.connection import S3Connection
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage, StaticFilesStorage)
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File

from .. import settings


logger = logging.getLogger(__name__)


class CachedS3FilesStorage(ManifestStaticFilesStorage):

    bucket_name = settings.AWS_STATIC_BUCKET_NAME

    def __init__(self, *args, **kwargs):
        base_url = settings.AWS_HOST_URL % {'bucket_name': self.bucket_name}
        super(CachedS3FilesStorage, self).__init__(
            base_url=base_url, *args, **kwargs)

    def post_process(self, paths, dry_run=False, **options):
        try:
            aws_keys = (
                settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        except AttributeError:
            raise ImproperlyConfigured(
                'Static collection requires '
                'AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY.')
        conn = S3Connection(*aws_keys)
        bucket = conn.get_bucket(self.bucket_name)

        bucket_files = [key.name for key in bucket.list()]

        post_process_generator = super(
            CachedS3FilesStorage, self).post_process(
                paths, dry_run=False, **options)
        self.hashed_files = OrderedDict()
        for name, hashed_name, processed in post_process_generator:
            if not hashed_name:
                logger.warning(
                    "Hashed name does not exist. Processed file '%s'. %s",
                    name, processed)
                continue
            hash_key = self.hash_key(name)
            self.hashed_files[hash_key] = hashed_name
            processed = False
            if hashed_name not in bucket_files:
                file_key = bucket.new_key(hashed_name)
                mime_type, encoding = mimetypes.guess_type(name)
                headers = {
                    'Content-Type': mime_type or 'application/octet-stream',
                    'Cache-Control': 'max-age=%d' % (3600 * 24 * 365,)}

                with self.open(hashed_name) as hashed_file:
                    file_key.set_contents_from_file(
                        hashed_file, policy=settings.AWS_POLICY,
                        replace=False, headers=headers)
                processed = True
            yield name, hashed_name, processed
        self.save_manifest()

    def hashed_name(self, name, content=None):
        try:
            return super(CachedS3FilesStorage, self).hashed_name(
                name, content=content)
        except ValueError:
            logger.warning(u'%s does not exist', name)
            return name


class S3MediaStorage(StaticFilesStorage):

    bucket_name = settings.AWS_MEDIA_BUCKET_NAME

    @property
    def bucket(self):
        try:
            aws_keys = (
                settings.AWS_MEDIA_ACCESS_KEY_ID,
                settings.AWS_MEDIA_SECRET_ACCESS_KEY)
        except AttributeError:
            raise ImproperlyConfigured(
                'Static collection requires '
                'AWS_MEDIA_ACCESS_KEY_ID and AWS_MEDIA_SECRET_ACCESS_KEY.')
        conn = S3Connection(*aws_keys)
        return conn.get_bucket(self.bucket_name)

    def _save(self, name, content):
        file_key = self.bucket.new_key(name)

        mime_type, encoding = mimetypes.guess_type(name)
        headers = {
            'Content-Type': mime_type or 'application/octet-stream',
            'Cache-Control': 'max-age=%d' % (3600 * 24 * 365,)}

        file_key.set_contents_from_file(
            content, headers=headers, policy=settings.AWS_POLICY, rewind=True)

        return name

    def _open(self, name, mode='rb'):
        temp_file = TemporaryFile()
        self.bucket.get_key(name).get_file(temp_file)
        return File(temp_file)

    def url(self, name):
        host = settings.AWS_HOST_URL % {'bucket_name': self.bucket_name}
        return host + name.split('?')[0]
