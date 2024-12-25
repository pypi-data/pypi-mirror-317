import ujson

from caasm_grpc_client._base import BaseGRPClient
from caasm_grpc_client.protos.meta_data.meta_data_pb2 import (
    google_dot_protobuf_dot_empty__pb2,
    TransformTestRequest,
    TransformRequest,
    TransformInitRequest,
    QueryStorageTableRequest,
    StorageToESRequest,
)
from caasm_grpc_client.protos.meta_data.meta_data_pb2_grpc import MetaDataStub


class MetaDataClient(BaseGRPClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._transform_init = False
        self._stub: MetaDataStub

    @property
    def stub_define(self):
        return MetaDataStub

    def ping(self):
        response = self.stub.Ping(google_dot_protobuf_dot_empty__pb2.Empty())
        return response.code

    def transform_init(self, category):
        self._stub.TransformInit(TransformInitRequest(categoryName=category))
        self._transform_init = True

    def transform_test(self, category, model_name, data, date):
        test_request = TransformTestRequest(
            categoryName=category,
            modelName=model_name,
            data=ujson.dumps(data, default=str),
            date=date,
        )
        response = self._stub.TransformTest(test_request)
        if not response.code:
            return self.build_response(code=response.code, message=response.message, data=None)
        return self.build_response(code=response.code, message="", data=ujson.loads(response.data))

    def find_storage_table(self, category):
        request = QueryStorageTableRequest(category=category)
        response = self._stub.FindStorageTable(request)
        return response.tableMapper

    def storage_to_query_engine(self, category, date):
        request = StorageToESRequest(category=category, date=date)
        response = self._stub.StorageToES(request)
        return response.code

    def transform_batch(self, category, model_name, data, date):
        if not self._transform_init:
            self.transform_init(category)
        transform_batch_request = TransformRequest(
            categoryName=category,
            modelName=model_name,
            data=[ujson.dumps(i, default=str) for i in data],
            date=date,
        )
        return self._stub.Transform(transform_batch_request)
