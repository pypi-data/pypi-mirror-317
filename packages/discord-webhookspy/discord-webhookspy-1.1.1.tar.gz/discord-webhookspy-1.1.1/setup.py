from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name="discord-webhookspy",  # Paketinizin adı
    version="1.1.1",
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
    long_description=description,
    long_description_content_type='text/markdown',
)
