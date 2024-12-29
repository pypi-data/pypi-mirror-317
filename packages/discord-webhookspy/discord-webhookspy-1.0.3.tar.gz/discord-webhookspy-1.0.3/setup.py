from setuptools import setup, find_packages

setup(
    name="discord-webhookspy",  # Paketinizin adı
    version="1.0.3",
    description="A simple Python library for Discord webhooks",
    author="AlperenS",
    author_email="ajaxseson1@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",  # Bağımlılıkları buraya ekleyin
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
