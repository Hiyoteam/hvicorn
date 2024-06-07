from setuptools import setup, find_packages

setup(
    name="hvicorn",
    version="0.0.4",
    description="Something for creating webapps like uvicorn, But for online chatrooms...",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hiyoteam/hvicorn",
    author="0x24a",
    author_email="admin@thz.cool",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="bot hack.chat hack.chat-bot",
    packages=find_packages(".", include=["hvicorn", "hvicorn.*"]),
    install_requires=[
        "websocket-client==1.8.0",
        "pydantic==2.7.3",
        "setuptools==70.0.0",
    ],
)
