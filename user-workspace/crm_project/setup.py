from setuptools import setup, find_packages
from os import path

# Read the contents of README.md
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='django-crm-project',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A comprehensive CRM system built with Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/django-crm-project',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Office/Business :: Groupware',
        'Topic :: Office/Business :: Scheduling',
    ],
    install_requires=requirements,
    python_requires='>=3.8',
    extras_require={
        'dev': [
            'pytest>=8.0.2',
            'pytest-django>=4.8.0',
            'factory-boy>=3.3.0',
            'coverage>=7.4.3',
            'black>=24.2.0',
            'flake8>=7.0.0',
            'isort>=5.13.2',
        ],
        'prod': [
            'gunicorn>=21.2.0',
            'psycopg2-binary>=2.9.9',
            'sentry-sdk>=1.40.6',
        ],
    },
    entry_points={
        'console_scripts': [
            'crm-project=crm_project.manage:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/django-crm-project/issues',
        'Source': 'https://github.com/yourusername/django-crm-project',
        'Documentation': 'https://django-crm-project.readthedocs.io/',
    },
)