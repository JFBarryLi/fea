from setuptools import setup, find_packages

setup(
    name='fea-app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask==1.1.2',
    ],
)
