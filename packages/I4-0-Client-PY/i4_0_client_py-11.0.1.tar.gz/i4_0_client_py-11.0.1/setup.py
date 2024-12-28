from setuptools import setup, find_packages

setup(
    name = "I4_0-Client-PY",
    version = "11.0.1",
    description = "Client Python bindings for I4.0.",
    author = "TAO71-AI",
    url = "https://github.com/TAO71-AI/I4.0",
    packages = find_packages(),
    license = "TAO71 I4.0 License (v1)",
    install_requires = [
        "websockets==13.1",
        "asyncio",
        "pyaudio"
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3.8",
    project_urls = {
        "Source": "https://github.com/TAO71-AI/I4.0",
        "License": "https://github.com/TAO71-AI/I4.0/blob/main/LICENSE.md"
    }
)
