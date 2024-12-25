from setuptools import setup, find_packages

setup(
    name='texconv',  
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'os',
        'subprocess',
        'datetime'
    ],
    author='Omkar Tasgaonkar',  
    author_email='rakmot19@gmail.com',
    description='Converting python to LaTeX',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)
 