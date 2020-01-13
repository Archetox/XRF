import setuptools

setuptools.setup(
    name="h5conversion",
    version="1.1.0",
    author="David Kuter",
    author_email="david.kuter@gmail.com",
    description="Converts CLS data to h5 files",
    long_description="Converts CLS XRF maps from tab-delimited dat files into h5 files so they can be opened in pyXRF",
    url="https://github.com/davidkuter/XRF/tree/master/",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={'console_scripts': ['h5conversion = h5conversion:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use  ",
        "Operating System :: Unix  ",
    ],
)