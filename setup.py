from setuptools import setup, find_packages

setup(
    name             = 'lambdagram',
    version          = '0.9.2',
    description      = 'telegram bot wrapper with webhook for aws lambda',
    long_description = open('README.md').read(),
    author           = 'Jaewoong',
    author_email     = 'jaewoong.go@gmail.com',
    url              = 'https://github.com/jwkcp/lambdagram',
    download_url     = 'https://pypi.org/project/lambdagram/#files',
    install_requires = ['requests'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['telegram', 'aws', 'lambda'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)