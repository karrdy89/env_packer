import logging
import traceback
import os
from logging import Logger

from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import response_vo as res_vo
import request_vo as req_vo
from _constants import RequestResult, PYTHON_VERSIONS, ModelStore
from s3_uploader import S3Uploader
from packing_util import create_envpack

app = FastAPI()
router = InferringRouter()


@cbv(router)
class BaseRouter:
    def __init__(self):
        self._worker = type(self).__name__
        self._logger: Logger = logging.getLogger("root")
        self._s3: S3Uploader = S3Uploader()

    @router.post("/envpack/upload", response_model=res_vo.Base)
    def upload_envpack(self, req_body: req_vo.UploadEnv):
        result_msg = res_vo.Base(CODE=RequestResult.SUCCESS, ERROR_MSG='')
        code, msg, path = create_envpack(env_name=req_body.CONVERTER_ID, packages=req_body.PACKAGES,
                                         python=req_body.PYTHON_VER)
        if code != 0:
            result_msg.CODE = RequestResult.FAIL
            result_msg.ERROR_MSG = "failed to make venv for python backend"
            self._logger.error(f"failed to make venv for python backend. {msg}")
        else:
            target_path = f"{req_body.PATH}/{path.split('/')[-1]}"
            try:
                self._s3.upload(bucket=ModelStore.BASE_PATH, source_path=path, target_path=target_path)
            except Exception as e:
                self._logger.error(f"{e.__str__()}, {traceback.format_exc()}")
                result_msg.CODE = RequestResult.FAIL
                result_msg.ERROR_MSG = "failed to upload venv for python backend"
        if os.path.exists(path):
            os.remove(path)
        return result_msg

    @router.get("/envpack/backend/pythons", response_model=res_vo.ListBackends)
    def get_pythons(self):
        result_msg = res_vo.ListBackends(CODE=RequestResult.SUCCESS, ERROR_MSG='', BACKENDS=PYTHON_VERSIONS)
        return result_msg


app.include_router(router)
