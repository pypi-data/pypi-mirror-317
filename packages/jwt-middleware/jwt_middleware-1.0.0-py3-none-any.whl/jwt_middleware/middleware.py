from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import jwt

class JWTMiddleware:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def __call__(self, request: Request, call_next):
        try:
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid or missing token")

            # Decode the JWT token
            decoded_token = jwt.decode(token.split(" ")[1], self.secret_key, algorithms=[self.algorithm])

            # Extract user_id from the token payload
            user_id = decoded_token.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: user_id not found")

            # Attach user_id to the request state for downstream usage
            request.state.user_id = user_id

            # Proceed to the next middleware or route handler
            response = await call_next(request)
            return response

        except HTTPException as e:
            # Return a JSON response with the error details
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})