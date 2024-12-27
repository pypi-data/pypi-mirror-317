from setuptools import setup, find_packages

setup(
    name='function_caller',
    version='0.1.2',  # Increment the version number for the new release
    description='Function calling for AI models without native support.',
    long_description_content_type='text/markdown',  # Specify the markup language
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