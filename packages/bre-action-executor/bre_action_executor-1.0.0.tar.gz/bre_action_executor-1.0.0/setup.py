from setuptools import setup, find_packages

setup(
    name='bre-action-executor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'requests',
    ],
    author='Miguel Cerqueira',
    author_email='miguel.cerqueira@netexlearning.com',
    description='Automate Action Executor',
    long_description='Library to execute actions in a workflow',
    long_description_content_type='text/markdown',
    url='https://github.com/netexknowledge/bre-action-executor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)