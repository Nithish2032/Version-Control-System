from setuptools import setup,find_packages
import ClientSide
setup(
    name="nit",
    version='1.3',
    author ="Nithish Kandepi",
    author_email = "nithish.kandepi@gmail.com",
    packages=["ClientSide","ClientSide/Local","ClientSide/Remote"],
    install_requires=[
        'click','checksumdir'
    ],
    entry_points='''
        [console_scripts]
        nit=ClientSide.main:main
    ''',
)


