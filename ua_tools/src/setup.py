from setuptools import find_packages, setup

setup(
    name='uatools',
    packages=find_packages(include=['uatools', 'logs']),
    version='1.0.0',
    description='UA tools is a collection of scripts automating tasks and providing report data',
    author='Vincent Corriveau',
    author_email='vincent.corriveau@cgi.com',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
