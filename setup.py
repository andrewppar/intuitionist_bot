from distutils.core import setup

setup(
    name='IntuitionisticBot', 
    author='Andrew Parisi', 
    author_email='andrew.p.parisi@gmail.com', 
    version='0.1dev', 
    packages=['intuitionistic_bot'], 
    install_requires=[ 
        'tweepy', 
        ], 
    long_description=open('README.md').read()
    )
