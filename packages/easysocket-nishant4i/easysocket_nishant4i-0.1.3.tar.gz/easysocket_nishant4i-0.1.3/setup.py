from setuptools import setup, find_packages

setup(
    name="easysocket-nishant4i",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "websockets>=10.0",
        "python-socketio>=5.0.0",
    ],
    extras_require={
        'flask': ['flask>=2.0.0', 'gevent-websocket>=0.10.1'],
        'django': ['django>=3.2', 'channels>=3.0.0'],
    },
    author="Nishant Maurya",
    author_email="mauryanishant2005@gmail.com",
    description="A simple WebSocket library for Flask and Django",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
) 