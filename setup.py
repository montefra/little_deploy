from setuptools import setup, find_packages


entry_points = {'console_scripts': ['little_deploy = little_deploy:main']}

setup(
    # package description and version
    name="little_deploy",
    version='0.0.0',
    author="Francesco Montesano",
    author_email="franz.bergesund@gmail.com",
    description="Copy files from one place to an other",
    long_description=open("README.md").read(),

    # list of packages and data
    packages=find_packages(),

    entry_points=entry_points,

    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: Unix",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Topic :: Software Development :: Documentation",
                 "Topic :: Utilities",
                 ]
)
