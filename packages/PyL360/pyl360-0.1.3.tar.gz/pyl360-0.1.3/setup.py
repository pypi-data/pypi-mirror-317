from setuptools import setup, find_packages

setup(
	name="PyL360",
	version="0.1.3",
	packages=find_packages(),
	install_requires=[
		"certifi==2024.12.14",
		"charset-normalizer==3.4.1",
		"dacite==1.8.1",
		"idna==3.10",
		"requests==2.32.3",
		"tls-client==1.0.1",
		"typing_extensions==4.12.2",
		"urllib3==2.3.0"
    ], 
	include_package_data=True,
	description="A package for interfacing with Life360",
	author="Sam Ramirez",
	url="https://github.com/arkangel-dev/py-life-360",
	classifiers=[
		"Programming Language :: Python :: 3"
	],
	python_requires=">=3.6",
)