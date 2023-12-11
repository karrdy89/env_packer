from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn

from _constants import ROOT_DIR, SYSTEM_ENV
from router import router


app = FastAPI()
app.include_router(router)
app.add_middleware(CORSMiddleware)

uv_conf = {"app": "start_server:app",
           "host": "0.0.0.0",
           "port": 7650,
           "log_config": ROOT_DIR+"/base_config/uv_log_config.ini"}


if SYSTEM_ENV.SSL_KEY_FILE and SYSTEM_ENV.SSL_CERT_FILE:
    base_cert_path = ROOT_DIR + "/cert/"
    uv_conf["ssl_keyfile"] = base_cert_path + SYSTEM_ENV.SSL_KEY_FILE
    uv_conf["ssl_certfile"] = base_cert_path + SYSTEM_ENV.SSL_CERT_FILE
    app.add_middleware(HTTPSRedirectMiddleware)
    if SYSTEM_ENV.SSL_CA_CERT_FILE:
        uv_conf["ssl_ca_certs"] = base_cert_path + SYSTEM_ENV.SSL_CA_CERT_FILE


config = uvicorn.Config(**uv_conf)


class UvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass


if __name__ == "__main__":
    pipeline_manager = PipelineManager()
    # service_state = ServiceState()# dev
    server = UvicornServer(config=config)
    server.run()
