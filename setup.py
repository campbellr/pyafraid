from setuptools import setup
import pyafraid

setup(
        name='pyafraid',
        version=pyafraid.__version__,
        description="Command-line tool for manipulating afraid.org DDNS",
        long_description=open('README').read(),
        py_modules=['pyafraid'],
        entry_points={'console_scripts': ['pyafraid = pyafraid:main']},
        author="Ryan Campbell",
        author_email="campbellr@gmail.com",
        url="http://github.com/campbellr/pyafraid",

        )
