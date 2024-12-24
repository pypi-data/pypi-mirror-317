from setuptools import setup, find_packages

setup(
    name='yh_olap',
    version='1.1.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'pyotp',
        'selenium',
        'webdriver_manager',
        'requests_toolbelt',
        'tenacity',
    ],
)