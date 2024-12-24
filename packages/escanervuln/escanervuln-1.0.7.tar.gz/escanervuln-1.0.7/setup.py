from setuptools import setup, find_packages

setup(
    name='escanervuln',
    version='1.0.7',
    description='Librería Modular de Detección de Vulnerabilidades en Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ignacio',
    author_email='knjasu098@gmail.com',
    url='https://github.com/tuusuario/escanervuln',
    packages=find_packages(),  # Asegura que el paquete sea incluido
    install_requires=[
        'flask',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'escanervuln=escanervuln.cli:main'  # Nombre del paquete y módulo correcto
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
