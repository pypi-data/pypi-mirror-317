from setuptools import setup, find_packages

setup(
    name='perceptive_crop_image',  # Package name
    version='2.0.0',  # Initial version
    packages=find_packages(),  # Automatically finds the packages
    install_requires=[  # External dependencies
        'numpy',
        'opencv-python',
    ],
    description='A manual cropping tool using OpenCV.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fathima',
    author_email='fathima.offical.msg@gmail.com',
    url='https://github.com/fathimaCode',  
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
