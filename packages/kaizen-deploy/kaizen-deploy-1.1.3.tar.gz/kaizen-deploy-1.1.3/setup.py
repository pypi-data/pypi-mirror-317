# -*- coding: utf-8 -*-

# python setup.py sdist
# twine upload dist/*

from setuptools import *


setup(
    name='kaizen-deploy',
    version='1.1.3',
    license='MIT',
    description="kaizen-deploy is a Configuration Management tool used for installing KIMS(Kubernetes Incident Management System anywhere.).",
    maintainer="Arjun Babu",
    maintainer_email='arbnair97@gmail.com',
    author="Arjun Babu",
    author_email='arbnair97@gmail.com',
    include_package_data=True,
    packages=['src', 'templates'],
    package_dir={'src': 'src', 'templates': 'src/templates'},
    package_data={'src': ['src/main.py'], 'templates': ['src/templates/manifest.yaml']},

    data_files=[
        ('Lib/kaizen-deploy', ['src/main.py']),
        ('Lib/kaizen-deploy/templates', ['src/templates/manifest.yaml'])],

    keywords='kaizen-deploy',
    
    classifiers=[
          'Development Status :: 5 - Production/Stable'
          ],

)
