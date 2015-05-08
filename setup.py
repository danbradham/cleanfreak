try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys
import cleanfreak


if sys.argv[-1] == 'cheeseit!':
    os.system('python setup.py sdist upload')
    sys.exit()


if sys.argv[-1] == 'testit!':
    os.system('python setup.py sdist upload -r test')
    sys.exit()


packages = [
    'cleanfreak',
    'cleanfreak.ui',
]

package_data = {
    '': ['LICENSE', 'README'],
    'cleanfreak': ['conf/*.*'],
}


with open('README.rst') as f:
    readme = f.read()


setup(
    name=cleanfreak.__title__,
    version=cleanfreak.__version__,
    description=cleanfreak.__description__,
    long_description=readme,
    author=cleanfreak.__author__,
    author_email=cleanfreak.__email__,
    url=cleanfreak.__url__,
    license=cleanfreak.__license__,
    packages=packages,
    package_data=package_data,
    package_dir={'cleanfreak': 'cleanfreak'},
    include_package_data=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
