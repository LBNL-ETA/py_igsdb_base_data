from setuptools import setup, find_packages

setup(
    name='py_igsdb_base_data',
    version='0.0.35',
    long_description='This library contains dataclasses to assist with IGSDB-related data and operations.',
    # tell setuptools to look for any packages under 'src'
    packages=find_packages(where='src'),
    # tell setuptools that all packages will be under the 'src' directory and nowhere else
    package_dir={'': 'src'},
    install_requires=['pydantic>=2.1.1',
                      'dataclasses-json==0.6.0'],
    test_suite='tests',
    zip_safe=False,
)
