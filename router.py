from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import response_vo as res_vo
import request_vo as req_vo
from _constants import REQUEST_RESULT
from s3_uploader import S3Uploader
from packing_util import create_envpack


app = FastAPI()
router = InferringRouter()


@cbv(router)
class BaseRouter:
    def __init__(self):
        self._worker = type(self).__name__
        self._s3: S3Uploader = S3Uploader()

    @router.post("/envpack/upload", response_model=res_vo.Base)
    def upload_envpack(self, req_body: req_vo.UploadEnv):
        result_msg = res_vo.Base(CODE=REQUEST_RESULT.SUCCESS, ERROR_MSG='')
        if req_body.PYTHON_VER is not None:
            code, msg = create_envpack(env_name=req_body.CONVERTER_ID, python_version=req_body.PYTHON_VER,
                                       packages=req_body.PACKAGES)
        else:
            code, msg = create_envpack(env_name=req_body.CONVERTER_ID, packages=req_body.PACKAGES)
        if code != 0:
            result_msg.CODE = REQUEST_RESULT.FAIL
            result_msg.ERROR_MSG = "failed to make venv for python backend"
        else:
            target_path = f"converters/{req_body.CONVERTER_ID}/{msg.split('/')[-1]}"
            try:
                self._s3.upload(bucket=req_body.PRJ_ID, source_path=msg, target_path=target_path)
            except Exception as e:
                result_msg.CODE = REQUEST_RESULT.FAIL
                result_msg.ERROR_MSG = "failed to upload venv for python backend"
        # delete file if exist
        return result_msg


app.include_router(router)
