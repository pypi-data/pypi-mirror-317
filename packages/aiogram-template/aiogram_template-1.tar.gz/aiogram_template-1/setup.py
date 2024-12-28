from setuptools import setup, find_packages

setup(
    name="aiogram_template",  # Loyihangizning nomi
    version="1",  # Versiya raqami
    packages=find_packages(),  # Paketlarni topish
    install_requires=[  # Kerakli kutubxonalar
        "aiogram",
        "environs" # Misol uchun
    ],
    author="Rafkix",
    author_email="rafkixuz@gmail.com",
    description="Aiogram3 kutubxonasi uchun template",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rafkix/Aiogram-3-TEmplate",  # GitHub yoki boshqa manzil
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)