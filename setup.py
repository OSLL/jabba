
from distutils.core import setup
from setuptools import find_packages

setup(
    name='jabba',
    packages=find_packages(exclude=['docs', 'doc', 'test']),
    version='0.1',
    description='Jenkins And Job Builder Analysis',
    author='Missingdays',
    author_email='rebovykin@gmail.com',
    url='https://github.com/OSLL/jenkins_job_builder_visualization',
    download_url='https://github.com/OSLL/jenkins_job_builder_visualization/arhive/0.1.tar.gz',
    keywords=['jenkins', 'job buider', 'visualization'],
    scripts=['bin/jabba'],
    classifiers=[]
)


