import os
import zipfile
from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name='h_ckpt',
    version='0.1',
    description='Protein chemical shift prediction based on Protein Language Model',
    author='Zhu He',
    author_email='2260913071@qq.com',
    url='https://github.com/doorpro/predict-chemical-shifts-from-protein-sequence.git',
    long_description = open('README.md',encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    zip_safe=True,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'reg_h': [
            'reg_h.pth'
        ]
    },
    entry_points = {
        'console_scripts': [
            'plm-cs=plm_cs.CS_predict:main'
        ]
    },
    install_requires=[
        'torch == 2.5.0',
        'torchaudio == 2.5.0',
        'torchvision == 0.20.0',
        'fair-esm == 2.0.0',
        'numpy == 2.1.2',
        'biopython == 1.84',
        'pandas == 2.2.3'
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
)