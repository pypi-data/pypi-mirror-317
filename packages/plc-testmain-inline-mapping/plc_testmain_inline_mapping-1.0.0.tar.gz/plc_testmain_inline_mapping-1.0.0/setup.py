from setuptools import setup 

with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 

REQUIREMENTS = [
	'pywin32>=306',
    'pyserial>=3'	
] 

CLASSIFIERS = [ 
	'Intended Audience :: Developers', 
	'Topic :: Software Development :: Libraries :: Python Modules',  
	'Programming Language :: Python :: 3', 
	] 

setup(name='plc_testmain_inline_mapping', 
	version='1.0.0', 
	description='Communication with PLC via serial connections', 
    long_description=long_description,
    long_description_content_type='text/x-rst',
	packages=['plc_module'], 
	classifiers=CLASSIFIERS, 
	install_requires=REQUIREMENTS, 
	keywords='communicates with PLC'
	) 