from setuptools import setup, find_packages

setup(
    name                           = "dma"                                                                                                  ,
    version                        = "1.0.6"                                                                                                ,
    description                    = "This Module Returns ASCII Art & Text in Many Different Variations Depending on The Called Function."  ,
    long_description_content_type  = "text/markdown"                                                                                        ,
    author                         = "Anvil"                                                                                                ,
    author_email                   = "_@chimera.rip"                                                                                        ,
    url                            = "https://github.com/vChimera/anvilly"                                                                  ,
    packages                       = find_packages()                                                                                        ,
    classifiers                    = [
        "Programming Language :: Python :: 3"                                                                                               ,
        "License :: OSI Approved :: MIT License"                                                                                            ,
        "Operating System :: OS Independent"                                                                                                ,
    ]                                                                                                                                       ,
    python_requires                = ">=3.6"                                                                                                ,
)