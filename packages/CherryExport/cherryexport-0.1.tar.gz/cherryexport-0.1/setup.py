from setuptools import setup, find_packages

setup(
    name='CherryExport',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'CherryExport': ['resources/*'],
    },
    install_requires=[
        'python-docx',
    ],
    entry_points={
        'console_scripts': [
            'CherryExport=CherryExport.log_export:main',
        ],
    },
)
