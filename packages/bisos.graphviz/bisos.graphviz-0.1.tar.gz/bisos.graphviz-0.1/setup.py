#!/usr/bin/env python

import setuptools
#import sys

####+BEGIN: bx:dblock:global:file-insert :mode python :file "/bisos/apps/defaults/begin/templates/purposed/pyModule/python/commonSetupCode.py"

import setuptools
import re
import inspect
import pathlib

def pkgName():
    """ From this eg., filepath=.../bisos-pip/PkgName/py3/setup.py, extract PkgName. """
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    grandMother = pathlib.Path(filename).resolve().parent.parent.name
    return f"bisos.{grandMother}"

def description():
    """ Extract title from ./README.org which is expected to have a title: line. """
    try:
        with open('./README.org') as file:
            while line := file.readline():
                if match := re.search(r'^#\+title: (.*)',  line.rstrip()):
                    return match.group(1)
                return "MISSING TITLE in ./README.org"
    except IOError:
        return  "ERROR: Could not read ./README.org file."

def longDescription():
    """ Convert README.org to README.rst. """
    try:
        import pypandoc
    except ImportError:
        result = "WARNING: pypandoc module not found, could not convert to RST"
        return result
    if (result := pypandoc.convert_file('README.org', 'rst')) is None:
        result = "ERROR: pypandoc.convert_file('README.org', 'rst') Failed."
    return result

####+END:


#__version__ = get_version('unisos/icm/__init__.py')
__version__ = '0.1'


requires = [
    'bisos.currents',
]

#print('Setting up under python version %s' % sys.version)
#print('Requirements: %s' % ','.join(requires))

scripts = [
]

setuptools.setup(
    name='bisos.graphviz',
    version=__version__,
    # namespace_packages=['bisos'],
    packages=setuptools.find_packages(),
    scripts=scripts,
    #data_files=data_files,
    # data_files=[
    #     ('pkgInfo', ["unisos/pkgInfo/fp/icmsPkgName/value"]),
    # ],
    #package_dir={'unisos.marme': 'unisos'},
    # package_data={
    #     'unisos.marme': ['pkgInfo/fp/icmsPkgName/value'],
    # },
    # package_data={
    #     '': ['unisos/marme/resolv.conf'],
    # },
    include_package_data=True,
    zip_safe=False,
    author='Mohsen Banan',
    author_email='libre@mohsen.1.banan.byname.net',
    maintainer='Mohsen Banan',
    maintainer_email='libre@mohsen.1.banan.byname.net',
    url='http://www.by-star.net/PLPC/180047',
    license='AGPL',
    description=description(),
    long_description=longDescription(),
    download_url='http://www.by-star.net/PLPC/180047',
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )

