# -*- coding: utf-8 -*-
"""
Redifest: Redshift Manifest Generator
---------------------------

Generate a .manifest file for given list of S3 buckets and PUT it to
a given S3 bucket

"""
from __future__ import print_function
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class ManifestGenerator(object):

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        """
        The Manifest Generator generates manifests generatively.

        The aws keys are not required if you have environmental params set
        for boto to pick up:
        http://boto.readthedocs.org/en/latest/s3_tut.html#creating-a-connection

        Parameters
        ----------
        aws_access_key_id: str
        aws_secret_access_key: str
        """
        if aws_access_key_id and aws_secret_access_key:
            self.conn = S3Connection()
        else:
            self.conn = S3Connection(aws_access_key_id, aws_secret_access_key)

    def _get_bucket_and_key(self, path):
        """Get top-level bucket and nested key path"""
        if '/' in path:
            parts = path.split('/')
            buckpath = parts[0]
            keypath = '/'.join(parts[1:])
        else:
            buckpath, keypath = path, ""
        return buckpath, keypath

    def generate_manifest(self, buckets, mandatory=True, path=None,
                          target=None):
        """
        Given a list of S3 buckets, generate a .manifest file (JSON format).

        You can pass in folders to the bucket argument, and this will
        only grab keys in those folders.

        Parameters
        ----------
        buckets: list
        mandatory: boolean
            The mandatory flag indicates whether the Redshift COPY should
            terminate if the file does not exist.
        path: str, default None
            Optional file path to write manifest file.
        target: str, default None
            Optional S3 path to write manifest file
        """
        manifest = {'entries': []}
        for buck in buckets:

            buckpath, keypath = self._get_bucket_and_key(buck)
            print('Getting bucket {}...'.format(buckpath))
            bukkit = self.conn.get_bucket(buckpath)

            print('Getting keys for bucket {} in key folder{}...'.format(
                buckpath, keypath
            ))
            for key in bukkit.list(keypath):
                manifest['entries'].append({
                    'url': '/'.join(['s3:/', key.bucket.name, key.name]),
                    'mandatory': mandatory
                    })

        if path:
            with open(path, 'w') as fp:
                json.dump(manifest, fp, sort_keys=True, indent=4)

        if target:
            self.write_manifest(manifest, target)

        return manifest

    def write_manifest(self, manifest, target=None):
        """
        Write a manifest to a given key

        Parameters
        ----------
        manifest: dict
        target: str
        bucket: Boto Bucket, default None
            If you already have a bucket, use that one
        """
        buckpath, keypath = self._get_bucket_and_key(target)
        print('Getting bucket {} for writing...'.format(target))
        bucket = self.conn.get_bucket(buckpath)

        key = Key(bucket, keypath)
        print("Writing manifest to {}".format(join(['s3://', key.bucket.name,
                                              key.name])))
        key.set_contents_from_string(
            json.dumps(manifest, sort_keys=True, indent=4)
        )
