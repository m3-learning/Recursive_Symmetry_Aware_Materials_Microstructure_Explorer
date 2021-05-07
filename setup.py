from setuptools import setup, find_packages

setup(
    name='Recursive_Symmetry_Aware_Materials_Microstructure_Explorer',
    version='0.0.10',
    packages=find_packages(where="src"),
    url='',
    license=' BSD-3-Clause',
    author='Tri N. M. Nguyen, Yichen Guo, Shuyu Qin, Joshua C. Agar',
    author_email='jca318@lehigh.edu',
    description='Tool for recursive symmetry aware searching of materials microstructure images',
    classifiers = [
                  "Programming Language :: Python :: 3",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
              ],
              package_dir = {"": "src"},
                            python_requires = ">=3.6",
)

