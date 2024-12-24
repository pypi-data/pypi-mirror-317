from pathlib import Path
from setuptools import find_packages, setup

# Package metadata
NAME = 'sale-price-house-prediction-adityalesmana'
DESCRIPTION = 'Sale price house prediction model package using regression from Train in Data'
URL = 'https://github.com/adityale1711/Sale-Price-Houses-Prediction'
EMAIL = 'a.lesmana1711@gmail.com'
AUTHOR = 'adityale1711'
REQUIRES_PYTHON = '>=3.6.0'

long_description = DESCRIPTION

# Load the package's VERSION file as a directory
about = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'sale_price_house_prediction_model'
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version

# packages are required for this module to be executed
def list_reqs(fname='requirements.txt'):
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().strip()

setup(
    name=NAME,
    version=about['__version__'],
    descriptions=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={'sale_price_house_prediction': ['VERSION']},
    install_requires=list_reqs(),
    extra_require={},
    include_package_data=True,
    license='BSD-3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)