
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tetrad_analysis", 
    version="0.0.1",
    author="Catherine_Harvey",
    author_email="harveycas@nih.gov",
    description="A package to help analyze tetrads",
    long_description= "A package to facilitate analyzing the antibiotic markers of yeast tetrads",
    long_description_content_type="text/markdown",
    url="https://github.com/harveycas/project_spring_2020",
    packages=setuptools.find_packages(),
    install_requires =['xlsxwriter'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)

