# jwt_middleware

A module for a middleware for our JWT token decryption. 

Will throw a HTTP exception code 401 in case of missing token, token expiration or invalid token. 

## Installation 
`pip3 install jwt-middleware`

## Usage
```
from fastapi import FastAPI
from jwt_middleware import JWTMiddleware

app = FastAPI()

# Add the JWT middleware
app.middleware("http")(JWTMiddleware(secret_key="your-secret-key"))

@app.get("/")
async def root():
    return {"message": "Welcome, authorized user!"}
```

## Publish a new version 
Pre-requisites: 
```
pip3 install setuptools
pip3 install wheel
pip3 install twine
```

1. Update the version number in setup.py 
2. Build the package: 
```
python3 setup.py sdist bdist_wheel
```
3. Verify the package: 
```
twine check dist/*
```
4. Publish the package: 
```
twine upload dist/*
```