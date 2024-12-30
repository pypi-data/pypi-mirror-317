from setuptools import setup, find_packages

setup(
    name                           = "770"                                                             ,
    version                        = "1.0.0"                                                           ,
    description                    = "This Module Creates a Purple Fade Effect on ASCII Art and Text." ,
    long_description               = open("README.md").read()                                          ,
    long_description_content_type  = "text/markdown"                                                   ,
    author                         = "Anvil"                                                           ,
    author_email                   = "_@chimera.rip"                                                   ,
    url                            = "https://github.com/vChimera/770"                                 ,
    packages                       = find_packages()                                                   ,
    classifiers                    = [
        "Programming Language :: Python :: 3"                                                          ,
        "License :: OSI Approved :: MIT License"                                                       ,
        "Operating System :: OS Independent"                                                           ,
    ]                                                                                                  ,
    python_requires                = ">=3.6"                                                           ,
)
