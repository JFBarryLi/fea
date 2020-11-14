from setuptools import setup, find_packages

setup(
    name='fea-app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi==0.61.2',
        'uvicorn==0.12.2',
        'pytest==6.1.1',
        'numpy==1.19.2',
    ],
)
