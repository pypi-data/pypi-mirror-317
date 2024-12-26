from setuptools import setup, find_packages

setup(
    name="jwt-middleware",
    version="1.0.0",
    description="JWT Middleware for FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Isa",
    author_email="isa@soberly.io",
    url="https://gitlab.com/soberly/backend/modules/jwt_middleware",  # Update with your repo URL
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.70.0",
        "PyJWT>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)