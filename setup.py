from setuptools import setup, find_packages

from composite_pk import __version__

extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
    'pytest-django>=3',
    'psycopg2',
]
extra_dev = [
    *extra_test,
]

extra_ci = [
    *extra_test,
    'python-coveralls',
]

setup(
    name='django-composite-pk',
    version=__version__,
    description='Composite primary key for Django.',

    url='https://github.com/SelfHacked/django-composite-pk',
    author='SelfDecode',
    author_email='zheng@selfdecode.com',

    packages=find_packages(),

    python_requires='>=3.6',

    install_requires=[
        'django>=2',
        'django-model-wrappers @ https://github.com/SelfHacked/django-model-wrappers/archive/master.zip',
        'returns-decorator',
    ],

    extras_require={
        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

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
