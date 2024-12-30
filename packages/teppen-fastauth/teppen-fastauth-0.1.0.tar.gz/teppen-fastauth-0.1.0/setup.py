from setuptools import setup, find_packages

setup(
    name='teppen-fastauth',
    version='0.1.0',
    author='Yasufumi Kamiyama',
    description='Authentication Library for FastAPI',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'PyJWT',
        'cryptography',
    ],
    license='MIT',
)
