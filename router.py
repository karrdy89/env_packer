from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import response_vo as res_vo
from _constants import REQUEST_RESULT


app = FastAPI()
router = InferringRouter()


@cbv(router)
class BaseRouter:
    def __init__(self):
        self._worker = type(self).__name__
        self._

    @router.post("/envpack/upload", response_model=res_vo.Base)
    def upload_envpack(self):
        result_msg = res_vo.Base(CODE=REQUEST_RESULT.SUCCESS, ERROR_MSG='')
        return result_msg


app.include_router(router)
