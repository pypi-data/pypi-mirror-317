from setuptools import setup, find_packages

setup(
    name='Radial-Bias',
    version='0.1.2',
    description='A simple Python project library.',
    author='Raunak',
    author_email='raunakgola9082@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[ "requests >=2.25.1",
    "numpy >=1.20.0"],  # List your dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
