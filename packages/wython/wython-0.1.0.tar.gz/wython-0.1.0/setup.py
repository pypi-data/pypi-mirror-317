from setuptools import setup, find_packages

setup(
    name='wython',
    version='0.1.0',
    description='An enhanced version of python (for fun)',
    author='Jiananlan',
    author_email='jal2024@139.com',
    url='https://github.com/',
    packages=find_packages(),
    install_requires=[
        "python-docx", "Pillow"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    include_package_data=False,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
