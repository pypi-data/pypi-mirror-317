from setuptools import setup, find_packages

setup(
    name='Moral88',
    version='0.2.0',
    description='A library for regression evaluation metrics.',
    author='Morteza Alizadeh',
    author_email='alizadeh.c2m@gmail.com',
    # url='https://github.com/yourusername/morteza',
    packages=find_packages(),
    install_requires=['numpy'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
