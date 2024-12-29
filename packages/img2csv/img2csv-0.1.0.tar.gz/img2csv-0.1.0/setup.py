from setuptools import setup, find_packages

setup(
    name='img2csv',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'img2csv=img2csv.img2csv:img2csv',
        ],
    },
    author='Dr.Majeed Jamakhani',
    author_email='mjbioinfo@gmail.com',
    description='A package to convert images paths to CSV',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MJBioInfo/img2csv',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
