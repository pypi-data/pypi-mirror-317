from setuptools import setup, find_packages

setup(
    name='paynowqr',
    version='0.1',
    packages=find_packages(),
    install_requires=["qrcode[pil]"],
    description='A simple python library to generate PayNow QR codes',
    author="Evan Khee",
    author_email="evankhee@ymail.com",
    url="",
)