from setuptools import setup, find_packages

setup(
    name='temp-user-manager',
    version='0.1.0',
    description='A package to manage temporary database users and permissions.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(include=['temp_user_manager', 'temp_user_manager.*']),
    install_requires=[
        'psycopg2-binary'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
