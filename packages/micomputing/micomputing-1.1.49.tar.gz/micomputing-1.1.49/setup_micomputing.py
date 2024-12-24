from setuptools import setup, find_packages

setup(
	name = 'micomputing',
	version = '1.1.49',
	keywords = ['pip', 'pymyc', 'micomputing', 'medical image', 'image registration', 'image similarities'],
	description = "'micomputing' is a package for medical image computing. ",
	long_description = '# MIComputing\n\n## Introduction\n\nPackage [`micomputing`](https://github.com/Bertie97/pycamia/tree/main/micomputing) is the medical image processing package under project [`PyCAMIA`](https://github.com/Bertie97/pycamia). It handles medical image read write, image interpolation, transformation, registration and so on. This package works under `PyCAMIA` and use `batorch.Tensor` as its basic data format. \n\n## Installation\n\nThis package can be installed by `pip install micomputing` or moving the source code to the directory of python libraries (the source code can be downloaded on [github](https://github.com/Bertie97/pycamia) or [PyPI](https://pypi.org/project/micomputing/)). \n\n```shell\npip install micomputing\n```\n\n\n\n## Acknowledgment\n\n@Yuncheng Zhou: Developer\n',
	long_description_content_type = 'text/markdown',
	license = 'MIT Licence',
	url = 'https://github.com/Bertie97/PyZMyc/micomputing',
	author = 'Yuncheng Zhou',
	author_email = 'bertiezhou@163.com',
	packages = find_packages(),
	include_package_data = True,
	platforms = 'any',
	install_requires = ['numpy', 'torch>=1.5.1', 'batorch', 'matplotlib', 'pycamia', 'pyoverload', 'nibabel', 'pydicom', 'SimpleITK']
)
