#!/usr/bin/env python3
import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'deuxcentdeuxhome_phal_plugin_wifi_setup', 'version.py')
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


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def get_description():
    with open(os.path.join(BASEDIR, "README.md"), "r") as f:
        long_description = f.read()
    return long_description


# Nom pip ET nom d'entry point préfixés 202home- (fork maison, archivé côté
# amont — voir stack/manifeste.yaml, section forks). Le MODULE Python, lui,
# ne peut pas commencer par un chiffre (SyntaxError) : "deuxcentdeuxhome",
# pas "202home", pour l'import réel — même contrainte, même solution que
# 202home-satellite-guard (son module s'appelle satellite_guard, sans le
# préfixe). Avant ce renommage, le nom pip ET l'entry point étaient
# identiques à l'amont — ambigu si jamais les deux se retrouvaient
# installés côte à côte, aucun moyen de distinguer lequel est chargé.
PLUGIN_ENTRY_POINT = '202home-phal-plugin-wifi-setup=deuxcentdeuxhome_phal_plugin_wifi_setup:WifiSetupPlugin'
setup(
    name='202home-phal-plugin-wifi-setup',
    version=get_version(),
    description='Fork 202home de ovos-PHAL-plugin-wifi-setup (archivé côté amont)',
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/aofc/ovos-PHAL-plugin-wifi-setup',
    author='Aiix',
    author_email='aix.m@outlook.com',
    license='Apache-2.0',
    packages=['deuxcentdeuxhome_phal_plugin_wifi_setup'],
    package_data={'': package_files('deuxcentdeuxhome_phal_plugin_wifi_setup')},
    install_requires=required("requirements.txt"),
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={'ovos.plugin.phal': PLUGIN_ENTRY_POINT}
)
