from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='image_oc',
	version='1.0.0',
	description='Simplifies image manipulation in Python using Pillow',
	long_description=long_description,
	long_description_content_type='text/markdown',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/image-oc',
		'Tracker': 'https://github.com/ouroboroscoding/image-oc/issues'
	},
	keywords=['image','pillow'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['image'],
	python_requires='>=3.10',
	install_requires=[
		'piexif>=1.1.3,<1.4',
		'pillow>=11.0.0,<11.1',
		'tools-oc>=1.2.4,<1.3'
	],
	zip_safe=True
)