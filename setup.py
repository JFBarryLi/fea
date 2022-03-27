from setuptools import setup, find_packages

setup(
    name='fea-app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi==0.65.2',
        'uvicorn==0.12.2',
        'pytest==6.1.1',
        'numpy==1.21.0',
        'requests==2.25.0',
        'gunicorn==20.0.4',
        'rich==9.4.0',
    ],
)
