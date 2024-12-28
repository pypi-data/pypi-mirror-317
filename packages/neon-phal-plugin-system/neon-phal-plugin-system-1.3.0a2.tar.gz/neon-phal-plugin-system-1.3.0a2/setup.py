#!/usr/bin/env python3
import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version_file = os.path.join(BASEDIR, 'neon_phal_plugin_system',
                                'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


def get_description():
    with open(os.path.join(BASEDIR, "README.md"), "r") as f:
        long_description = f.read()
    return long_description

PLUGIN_ENTRY_POINT = 'neon-phal-plugin-system=neon_phal_plugin_system:SystemEventsPlugin'
ADMIN_ENTRY_POINT = 'neon-phal-plugin-system=neon_phal_plugin_system:SystemEventsAdminPlugin'
setup(
    name='neon-phal-plugin-system',
    version=get_version(),
    description='A plugin for OVOS/Neon hardware abstraction layer',
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/NeonGeckoCom/neon-phal-plugin-system',
    author='NeonGecko',
    author_email='developers@neon.ai',
    license='Apache-2.0',
    packages=['neon_phal_plugin_system'],
    package_data={'': package_files('neon_phal_plugin_system')},
    install_requires=required("requirements.txt"),
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
entry_points={
        'ovos.plugin.phal': PLUGIN_ENTRY_POINT,
        'ovos.plugin.phal.admin': ADMIN_ENTRY_POINT}
)
