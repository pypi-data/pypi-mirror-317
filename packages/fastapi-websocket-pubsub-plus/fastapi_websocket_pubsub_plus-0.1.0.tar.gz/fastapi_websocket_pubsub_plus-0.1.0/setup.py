from setuptools import setup, find_packages


def get_requirements(env=""):
    if env:
        env = "-{}".format(env)
    with open("requirements{}.txt".format(env)) as fp:
        return [x.strip() for x in fp.read().split("\n") if not x.startswith("#")]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastapi_websocket_pubsub_plus",
    version="0.1.0",
    author="Vishal Singh Baraiya",
    author_email="realvixhal@gmail.com",
    description="A fast and durable PubSub channel over Websockets (using fastapi-websockets-rpc).",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/vishal-singh-baraiya/fastapi_websocket_pubsub_plus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi-websocket-rpc>=0.1.25,<1",          # FastAPI WebSocket RPC, version range
        "packaging>=20.4",                           # Packaging library, minimum version 20.4
        "permit-broadcaster[redis,postgres,kafka]>=0.2.5,<3",  # Permit broadcaster with extras
        "pydantic>=1.9.1",                           # Pydantic, minimum version 1.9.1
        "websockets>=10.3",                          # Websockets, minimum version 10.3
    ],
)
