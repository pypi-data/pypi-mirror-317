from setuptools import setup, find_packages

setup(
	name = "print_helper_logger",
	version = "0.0.4",
	packages = find_packages(),
	install_requires = [],
	author = "Oscar Gomez Fuente",
	author_email = "oscargomezf@gmail.com",
	description = 'Package for printing messages to the console and to the system logger',
	long_description = open("README.md").read(),
	long_description_content_type = "text/markdown",
	url = "https://github.com/oscargomezf/python_tools/print_helper_logger",
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires = '>=3.6',
)
