from setuptools import setup, find_packages

setup(
    name='function_caller', 
    version='0.1.0',
    description='Function calling for AI models without native support.',
    author='Devs Do Code (Sree)',
    author_email='devsdocode@gmail.com', 
    url='https://github.com/SreejanPersonal/function_caller', 
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorlog',
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)