from setuptools import setup, find_packages

from composite_pk import __version__

setup(
    name='django-composite-pk',
    version=__version__,
    description='Composite primary key for Django.',

    author='SelfDecode',
    author_email='zheng@selfdecode.com',

    packages=find_packages(),

    install_requires=[
        'django>=2',
    ],

    classifiers=[
        'Intended Audience :: Developers',

        'Development Status :: 3 - Alpha',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
