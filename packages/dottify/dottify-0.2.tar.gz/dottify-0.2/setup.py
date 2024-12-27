from setuptools import setup, find_packages

setup(
    name='dottify',
    version='0.1',
    packages=find_packages(),
    description=(
        'Dottify est une bibliothèque Python simple qui '
        'permet de convertir des dictionnaires en objets '
        'accessibles par attributs. Au lieu d\'utiliser '
        'la syntaxe classique dict[\'key\'], vous pouvez '
        'accéder aux valeurs d\'un dictionnaire en '
        'utilisant la notation par points dict.key après '
        'avoir appliqué la transformation.'
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nana Elie',
    author_email='elienana92@gmail.com',
    url='https://github.com/nanaelie/dottify',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)
