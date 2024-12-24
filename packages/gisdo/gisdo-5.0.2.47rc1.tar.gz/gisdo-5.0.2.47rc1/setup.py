# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.bdist_egg import walk_egg

from distutils import log


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


class bdist_safe_egg(bdist_egg):
    description = "create an \"egg\" distribution with source files" \
                  " for management commands"

    def run(self):
        bdist_egg.run(self)
        log.info(self.egg_output)

    def zap_pyfiles(self):
        is_management_command = lambda path: (
            'management%scommands' % os.sep) in path

        log.info("Removing .py files from temporary directory")
        for base, dirs, files in walk_egg(self.bdist_dir):
            if is_management_command(base):
                continue
            for name in files:
                if name.endswith('.py'):
                    path = os.path.join(base, name)
                    log.debug("Deleting %s", path)
                    os.unlink(path)

setup(
    name="gisdo",
    version='5.0.2.47rc1',
    description=read('DESCRIPTION'),
    license="GPL",
    keywords="kinder gisdo",
    scripts=[
        'scripts/create_mock_server.py',
        'scripts/gisdo_checklist_tests.py',
    ],
    url="https://src.bars-open.ru/py/WebEdu/kinder_contrib/gisdo",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['example', 'example.*']),
    install_requires=['SQLAlchemy==0.9.4'],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    cmdclass={
        'bdist_safe_egg': bdist_safe_egg
    },
)
