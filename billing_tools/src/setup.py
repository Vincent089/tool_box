from setuptools import find_packages, setup

setup(
    name='billingtools',
    packages=find_packages(include=['billingtools']),
    version='0.1.0',
    description='Billing tools simple exposer to various script automating some repeating task',
    author='Vincent Corriveau',
    author_email='vincent.corriveau@cgi.com',
    license='MIT',
    install_requires=['flask'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mypy', 'requests'],
    test_suite='tests',
)
