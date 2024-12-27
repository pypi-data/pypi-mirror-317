from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extensions = []
for root, _, files in os.walk("pyehandler"):
    for file in files:
        if file.endswith('.py') or file.endswith('.pyx'):
            path = os.path.join(root, file)
            module_path = path.replace(os.path.sep, '.')[:-3 if file.endswith('.py') else -4]
            extensions.append(Extension(module_path, [path]))

setup(
    name="pye-extension",
    version="0.1.1",
    author="oha",
    author_email="aaronoh2003@hotmail.com",
    description="Advanced Python code protection beyond pyc files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duriantaco/pye",
    packages=find_packages(),
    install_requires=[
        'cryptography>=41.0.0',
    ],
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'embedsignature': True,
            'binding': True
        }
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License", 
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.8",
    entry_points={  
        'console_scripts': [
            'pyehandler=pyehandler.cli:main',
        ],
    },
    license="Proprietary",
    license_files=("LICENSE",),
    
    package_data={
        'pyehandler': [
            '*.pyx.template',  
        ]
    },

    exclude_package_data={
        '': ['*.py', '*.pyx', '*.c', '*.h', '*.pxd'], 
        'pyehandler': ['*.py', '*.pyx', '*.c', '*.h', '*.pxd'], 
    },
    
    options={
        'bdist_wheel': {
            'py_limited_api': False,
        },
    },
    
    zip_safe=False
)