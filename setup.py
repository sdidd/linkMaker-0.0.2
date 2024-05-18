from setuptools import setup, find_packages

setup(
    name='temp_link_tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pyngrok',
        'werkzeug',
    ],
    entry_points={
        'console_scripts': [
            'temp-link=temp_link_tool.cli:main',
        ],
    },
)
