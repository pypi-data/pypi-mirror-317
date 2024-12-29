from setuptools import setup, find_packages

setup(
    name="SoftwareAI",  # Nome do pacote
    version="0.3.16",  # Versão inicial
    description="SoftwareAI is a framework with the aim of creating a software/application development company/organization governed by AI, its objective is not just to create the software with updates, documentation, schedules and spreadsheets, SoftwareAI is capable of running a software company completely with all the teams that make up a software company",
    long_description=open("READMEPIP.md", encoding="utf-8").read(),  # Codificação UTF-8
    long_description_content_type="text/markdown",
    author="ualers",
    author_email="freitasalexandre810@gmail.com",
    url="https://github.com/ualers/SoftwareAI",
    license="Apache License 2.0",
    packages=find_packages(),  # Encontra todos os pacotes automaticamente
    include_package_data=True,  # Inclui arquivos não-Python listados no MANIFEST.in
    install_requires=[
        "firebase-admin",
        "asyncio",
        "pandas",
        "tiktoken",
        "PyGithub",
        "requests",
        "python-dotenv",
        "gitpython",
        "openai"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",  # Classificador da licença Apache 2.0
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Versão mínima do Python
)
