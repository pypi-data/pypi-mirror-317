from setuptools import setup, find_packages

setup(
    name="Simple-Discord-Webhooks",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["urllib3"],
    description="A library to send Discord webhooks with advanced embed support.",
    author="qxod",
    url="https://github.com/imqxod/SimpleDiscordWebhooks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
