import io
import json

from minio.error import S3Error


class MinioWrapper:
    def __init__(self, minio_client, bucket_name=None):
        self.client = minio_client
        self.bucket_name = bucket_name

    def get_json(self, object_name):
        from minio import S3Error
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            object_data = response.read().decode('utf-8')
            response.close()
            response.release_conn()
            return json.loads(object_data)
        except S3Error as err:
            if err.code == 'NoSuchKey':
                return None
            raise err

    def object_exists(self, object_name):
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error as err:
            if err.code == 'NoSuchKey':
                return False
            raise

    def list_objects(self, prefix=None, recursive=False):
        return self.client.list_objects(self.bucket_name, prefix=prefix, recursive=recursive)

    def get_metadata(self, object_name):
        stat = self.client.stat_object(self.bucket_name, object_name)
        return stat.metadata

    def put_json(self, object_name, json_obj, metadata=None):
        data_bytes = io.BytesIO(json.dumps(json_obj, ensure_ascii=False, indent=2).encode("utf-8"))
        _len = data_bytes.getbuffer().nbytes
        self.client.put_object(self.bucket_name, object_name, data_bytes, length=_len, content_type="application/json", metadata=metadata)
        obj = self.client.stat_object(self.bucket_name, object_name)
        if obj.object_name != object_name:
            raise Exception("put data error")

    def put_object(self, object_name, data, content_type, metadata=None):
        data_bytes = io.BytesIO(data)
        _len = data_bytes.getbuffer().nbytes

        self.client.put_object(self.bucket_name, object_name, data_bytes, length=_len, content_type=content_type, metadata=metadata)
        obj = self.client.stat_object(self.bucket_name, object_name)
        if obj.object_name != object_name:
            raise Exception("put data error")

    def create_bucket(self, bucket_name):
        bucket_name = bucket_name or self.bucket_name
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
