"""
Lucheng is a forum software written in Python using the microframework Flask.

copy from FlaskBB

And Easy to Setup
-----------------
    $ pip install -e .

    $ flaskbb install

    $ flaskbb run

"""
from setuptools import setup, find_packages

setup(
    name='lucheng',
    version='1.0.dev0',
    license='BSD',
    author='Lucheng',
    author_email='cheng.lu@united-imaging.com',
    description='A classic Forum Software in Python using Flask.',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'click',
        'colorama',
        'flask',
        'SQLAlchemy',
        'SQLAlchemy-Utils',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-Login',
        'Flask-WTF',
        'Flask-Bootstrap'
    ],
    entry_points='''
        [console_scripts]
        lucheng=lucheng.cli:lucheng
    ''',
)
