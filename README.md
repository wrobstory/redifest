```
.------..------..------..------..------..------..------..------.
|R.--. ||E.--. ||D.--. ||I.--. ||F.--. ||E.--. ||S.--. ||T.--. |
| :(): || (\/) || :/\: || (\/) || :(): || (\/) || :/\: || :/\: |
| ()() || :\/: || (__) || :\/: || ()() || :\/: || :\/: || (__) |
| '--'R|| '--'E|| '--'D|| '--'I|| '--'F|| '--'E|| '--'S|| '--'T|
`------'`------'`------'`------'`------'`------'`------'`------'
```

Does what it says on the tin: Generates a [Redshift .manifest file](http://docs.aws.amazon.com/redshift/latest/dg/loading-data-files-using-manifest.html) given a list of S3 buckets. Can write said manifest to file, or back to S3.

API
___

Create a manifest generator with your AWS creds:

```python
>>> gen = ManifestGenerator('aws_access_key_id', 'aws_secret_access_key')
```

If following the [boto convention](http://boto.readthedocs.org/en/latest/s3_tut.html#creating-a-connection) for creds in env variables, you do not need to pass them in.

Generate a manifest:
```python
>>> manifest = gen.generate_manifest(['mybucket/folder1/folder2', 'mybucket/folder3'])

{'entries': [{'mandatory': True,
              'url': u's3://mybucket/folder1/folder2/foo.json'},
             {'mandatory': True,
              'url': u's3://mybucket/folder1/folder2/bar.json'},
             {'mandatory': True,
               'url': u's3://mybucket/folder3/bar.json'}]}
```

You can provide an optional path to write the manfifest back to S3 as part of the call
to generate the manifest:
```python
>>> gen.generate_manifest(['mybucket/folder1/folder2', 'mybucket/folder3'],
                          target='mybucket/manifest_files/qux.manifest')
```

Or write the dict you generated in `generate_manifest`:
```python
>>> gen.write_manifest(manifest, 'mybucket/manifest_files/qux.manifest')
```

You can also write to file:
```python
>>> gen.generate_manifest(['mybucket/folder1/folder2', 'mybucket/folder3'],
                          path='qux.manifest')
```
