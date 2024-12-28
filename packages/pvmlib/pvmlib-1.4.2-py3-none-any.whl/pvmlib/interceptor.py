from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from .models import Application, DefaultLogger, Measurement
from .logger import LoggerSingleton
from .response_exception import ResponseException
from .response_ok import ResponseOK
from .call_service_network import RestClient
from datetime import datetime
import traceback

class InterceptMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, app_info: Application, auth_service_url: str = None):
        super().__init__(app)
        self.app_info = app_info
        self.logger = LoggerSingleton().get_logger()
        self.auth_service_url = auth_service_url
        self.rest_client = RestClient(base_url=auth_service_url) if auth_service_url else None

    async def dispatch(self, request: Request, call_next):
        if "health" in request.url.path:
            return await call_next(request)

        start_time = datetime.now()
        measurement = Measurement(
            method=request.method,
            elapsedTime=0
        )

        response = None
        
        try:
            if self.rest_client is not None:
                token = request.headers.get("Authorization")
                if not token:
                    raise ResponseException(
                        http_status_code=401,
                        message="Authorization token missing",
                        error_code="AUTH_ERROR",
                        headers={"X-Request-ID": request.headers.get("X-Request-ID", "N/A")},
                    )

                auth_response = self.rest_client.post("/verificar-token", headers={"Authorization": token})
                if auth_response["status"] != 200:
                    raise ResponseException(
                        http_status_code=auth_response["status"],
                        message=auth_response["message"],
                        error_code="AUTH_ERROR",
                        headers={"X-Request-ID": request.headers.get("X-Request-ID", "N/A")},
                    )

            response = await call_next(request)
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000  # Convertir a milisegundos
            measurement.elapsedTime = int(elapsed_time)

            if response.status_code < 400:
                if hasattr(response, "json"):
                    response_data = await response.json()
                else:
                    response_data = await response.body()
                adapted_response = ResponseOK(
                    status_code=response.status_code,
                    message="Request processed successfully",
                    transaction_id=request.headers.get("X-Request-ID", "N/A"),
                    time_elapsed=measurement.elapsedTime,
                    data=response_data
                ).to_dict()
                response = JSONResponse(status_code=response.status_code, content=adapted_response)

            log_entry = DefaultLogger(
                level="INFO",
                schemaVersion="1.0.0",
                logType="TRANSACTION",
                sourceIP=request.client.host,
                status="SUCCESS",
                message="Request processed successfully",
                logOrigin="INTERNAL",
                timestamp=start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                tracingId=request.headers.get("X-Request-ID", "N/A"),
                hostname=request.url.hostname,
                eventType="REQUEST_PROCESSED",
                application=self.app_info,
                measurement=measurement,
                destinationIP="N/A",
                additionalInfo={"path": request.url.path}
            )

            self.logger.info(log_entry.json())
            return response

        except ResponseException as e:
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
            measurement.elapsedTime = int(elapsed_time)

            log_entry = DefaultLogger(
                level="ERROR",
                schemaVersion="1.0.0",
                logType="TRANSACTION",
                sourceIP=request.client.host,
                status="FAILURE",
                message=e.message,
                logOrigin="INTERNAL",
                timestamp=start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                tracingId=request.headers.get("X-Request-ID", "N/A"),
                hostname=request.url.hostname,
                eventType="REQUEST_FAILED",
                application=self.app_info,
                measurement=measurement,
                destinationIP="N/A",
                additionalInfo={"path": request.url.path, "stackTrace": traceback.format_exc().splitlines()}
            )

            self.logger.error(log_entry.json())
            response = JSONResponse(
                status_code=e.http_code,
                content=e.to_dict()
            )
            return response

        except Exception as e:
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000  # Convertir a milisegundos
            measurement.elapsedTime = int(elapsed_time)

            log_entry = DefaultLogger(
                level="ERROR",
                schemaVersion="1.0.0",
                logType="TRANSACTION",
                sourceIP=request.client.host,
                status="FAILURE",
                message=str(e),
                logOrigin="INTERNAL",
                timestamp=start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                tracingId=request.headers.get("X-Request-ID", "N/A"),
                hostname=request.url.hostname,
                eventType="REQUEST_FAILED",
                application=self.app_info,
                measurement=measurement,
                destinationIP="N/A",
                additionalInfo={"path": request.url.path, "stackTrace": traceback.format_exc().splitlines()}
            )

            self.logger.error(log_entry.json())
            response = JSONResponse(
                status_code=500,
                content=ResponseException(
                    http_status_code=500,
                    message="Internal Server Error",
                    error_code="INTERNAL_ERROR",
                    headers={"X-Request-ID": request.headers.get("X-Request-ID", "N/A")},
                ).to_dict()
            )
            return response