import requests
import io
import zipfile
from src.protobuild.exposurekey_pb2 import *


class ImmuniAPI:
    BASE_URL = "https://get.immuni.gov.it/v1/keys/"

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def _request(self, path, raw=False):
        r = requests.get(self.base_url + str(path))
        return r.json() if not raw else r.content

    def index(self):
        return self._request("index")

    def get_batch(self, batch_id):
        compressed_file = self._request(batch_id, raw=True)
        stream = io.BytesIO(compressed_file)
        input_zip = zipfile.ZipFile(stream)
        raw_teke = {name: input_zip.read(name) for name in input_zip.namelist()}['export.bin'][16:]
        return TemporaryExposureKeyExport().FromString(raw_teke)
