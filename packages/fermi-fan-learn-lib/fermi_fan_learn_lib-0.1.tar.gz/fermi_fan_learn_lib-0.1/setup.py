from setuptools import setup, find_packages

setup(
    name='fermi_fan_learn_lib',
    version='0.1',
    packages=find_packages(),
    install_requires=['None'],
    description='A library for Fermi-LAT FAN learning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='fengpeng',
    author_email='765915617@qq.com',
    url='https://github.com/fermi-fan/tutorial',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    )