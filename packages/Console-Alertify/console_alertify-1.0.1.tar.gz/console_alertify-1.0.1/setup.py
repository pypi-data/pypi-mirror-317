from setuptools import setup, find_packages

setup(
    name='Console-Alertify',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[],
    test_suite='tests',
    description="Una librería para mostrar mensajes coloridos y formateados en consola",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Carlos-dev-G/Console-Alertify",
    author="Carlos-dev-G",
    author_email="baa4tsdev@gmail.com",
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)