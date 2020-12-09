"""
flask-container-scaffold
-------------

A library to facilitate deploying flask applications easily in either a
container environment, development, or another production configuration
"""
from setuptools import setup


setup(
    name='flask-container-scaffold',
    version='1.0',
    url='http://github.com/release-depot/flask-container-scaffold',
    license='MIT',
    author='Jason Guiditta',
    author_email='jason.guiditta@gmail.com',
    description='Configuration layer to aid in deployment of Flask apps',
    long_description=__doc__,
    py_modules=['flask_container_scaffold'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
