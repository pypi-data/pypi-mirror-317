"""
hl7_tea
-----------
A package for manipulating HL7 data.
Link
`````
* Source
https://github.com/kouroshparsa/hl7_tea
"""
from setuptools import setup, find_packages

version = '1.0.2'
setup(
    name='hl7_tea',
    version=version,
    url='https://github.com/kouroshparsa/hl7_tea',
    download_url='https://github.com/kouroshparsa/hl7_tea/packages/%s' % version,
    license='GNU',
    author='Kourosh Parsa',
    author_email="kouroshtheking@gmail.com",
    description='A package for manipulating HL7 data.',
    long_description=__doc__,
    packages=find_packages(),
    install_requires = [],
    include_package_data=True,
    package_data = {'hl7_tea': []},
    zip_safe=False,
    platforms='all',
    classifiers=[
        'Programming Language :: Python',
    ]
)