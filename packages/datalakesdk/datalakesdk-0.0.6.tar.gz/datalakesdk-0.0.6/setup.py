import setuptools
from setuptools import find_packages

setuptools.setup(name='datalakesdk',
                 version="0.0.6",
                 description='DataLake SDK',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type="text/markdown",
                 author='ivan',
                 author_email='ivan.liu@anker-in.com',
                 url='',
                 # py_modules=['sdk'],
                install_requires=[
                    "requests==2.31.0",
                    "pydantic==2.9.2",
                    "hachoir==3.3.0"
                ],
                 license='MIT License',
                 zip_safe=False,
                 keywords='',
                 packages=find_packages()
)