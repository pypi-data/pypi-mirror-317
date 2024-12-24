from setuptools import setup, find_packages

setup(
    name='bsm_library01',  # Replace with your library name
    version='0.1.0',  # Version of your library
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[  # List your library's dependencies here
        # 'numpy',  # Example dependency
        'flask'
    ],
    author='JR',
    author_email='jefri.ronaldo@banksinarmas.com',
    description='Testing library for BSM AIDSU',
    # long_description=open('README.md').read(),  # Optional: long description from README
    # long_description_content_type='text/markdown',  # Optional: format of long description
    url='https://github.com/yourusername/my_library',  # URL to your library's repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change to your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Specify the Python version required
)