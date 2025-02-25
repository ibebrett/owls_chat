from setuptools import setup


setup(
    name="owls_chat",
    version="1.0",
    description="An experiment in internet",
    author="SCSU CS Club",
    packages=["owls_chat"],
    entry_points={
        "console_scripts": [
            "owls_chat_client=owls_chat.client:main",
            "owls_chat_server=owls_chat.server:main",
        ]
    },
)
