# setup.py

from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools import  find_namespace_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='nfkbin',
    version='1.0.0',
    description='NFkBin: Prediction of NF-Kbin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    author='Prof. G.P.S. Raghava',
    author_email='raghava@iiitd.ac.in',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'nfkbin.padel':['**/*'],
    'nfkbin.model':['*'],
    'nfkbin.molecules':['*']},
    entry_points={'console_scripts' : ['nfkbin = nfkbin.python_script.nfkbin:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires= [ 'numpy', 'pandas', 'scikit-learn', 'argparse' ,'tqdm' ]

)


