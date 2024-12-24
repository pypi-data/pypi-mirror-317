from setuptools import setup, find_packages

description = open('README.md', 'r', encoding='utf-8').read()

setup(
    name='localify',  # Nome del pacchetto
    version='0.1.0',  # Versione del pacchetto
    description='A lightweight i18n localization package for Python',  # Breve descrizione
    long_description= description,  # Descrizione lunga dal README
    long_description_content_type='text/markdown',  # Formato del README (Markdown)
    author='FeliceDev',  # Autore
    author_email='felicedev@outlook.com',  # Email dell'autore
    url='https://github.com/felicedev/localify',  # URL del repository
    packages=find_packages(),  # Trova automaticamente i pacchetti nella directory
    include_package_data=True,  # Include file non-Python come i JSON per le traduzioni
    install_requires=[],  # Nessuna dipendenza obbligatoria
    extras_require={
        'yaml': ['pyyaml'],  # Dipendenza opzionale per il supporto YAML
    },
    classifiers=[
        'Programming Language :: Python :: 3',  # Specifica Python 3
        'License :: OSI Approved :: MIT License',  # Tipo di licenza
        'Operating System :: OS Independent',  # Indipendente dal sistema operativo
    ],
    python_requires='>=3.6',  # Versione minima di Python
)
