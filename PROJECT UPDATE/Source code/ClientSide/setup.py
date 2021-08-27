from setuptools import setup,find_packages

setup(
    name="nit",
    version='1.0',
    author ="Nithish Kandepi",
    author_email = "nithish.kandepi@gmail.com",
    packages=find_packages(),
    install_requires=[
        'click',"checksumdir"
    ],
    entry_points='''
        [console_scripts]
        nit=main:main
    ''',
)


