from setuptools import setup, find_packages

setup(
    name='google_py_apis',
    version='0.1.8',
    author='Siddhant Kushwaha',
    author_email='k16.siddhant@gmail.com',
    description="Wrapper on google's REST APIs. As I use them a lot.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/siddhantkushwaha/GoogleAPIs',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'pycryptodome'
    ]
)
