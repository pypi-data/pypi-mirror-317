class LibraryInfo:
    version_lib = 'v1.4.2'
    name = 'pvmlib'
    author = "Jesus Lizarraga"
    author_email = "jesus.lizarragav@coppel.com"
    description = "Python library for PVM"
    python_requires = '>=3.12'
    env = 'development'
    
    install_requires = [
        "pydantic",
        "typing",
        "pytz",
        "logging",
        "circuitbreaker",
        "requests>=2.25.1,<3.0.0",
        "tenacity",
        "fastapi",
        "motor",
        "uvicorn",
        "urllib3>=1.26.5,<2.0.0",
        "charset_normalizer>=2.0.0,<3.0.0"
    ]