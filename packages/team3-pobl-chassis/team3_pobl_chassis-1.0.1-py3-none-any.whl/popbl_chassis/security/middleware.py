from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
from popbl_chassis.security.securityprovider import SecurityProvider


class AutenticationMiddleware:
    valid_routes = None
    ask_for_keys: bool= None
    generate_keys: bool = None
    role: str = None
    security_service: SecurityProvider = None

    @classmethod
    async def create(cls, valid_routes=None, ask_for_keys: bool = None, generate_keys: bool = None,role: str = None, security_service: SecurityProvider = None):
        self = AutenticationMiddleware()
        self.valid_routes = valid_routes
        self.ask_for_keys = ask_for_keys
        self.generate_keys = generate_keys
        self.security_service = security_service
        self.role = role
        return self
    
    async def dispatch(self, request: Request, call_next):
        for route_method, route_path in self.valid_routes:
            if route_path == request.url.path and (route_method is None or route_method == request.method):
                return await call_next(request)
        try:
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

            token = auth.split(" ")[1]
            payload = self.security_service.decode_token(token)

            if self.security_service.validar_fecha_expiracion(payload):
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})

            if not self.security_service.validate_role(payload, self.role):
                return JSONResponse(status_code=403, content={"detail": "Insufficient permissions"})

            response = await call_next(request)
            return response

        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        except Exception as exc:
            print(exc)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
