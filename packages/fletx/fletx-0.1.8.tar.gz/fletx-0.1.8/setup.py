from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = "fletx",
    version = "0.1.8",
    author="Saurabh Wadekar [ INDIA ]",
    packages=["fletx",'fletx.controls'],
    license="MIT",
    maintainer="Saurabh Wadekar",
    maintainer_email="saurabhwadekar420@gmail.com",
    keywords=["flet","routing","fletx","routes","state","flet app"],
    description="FletX is a powerful routing and state management library for the Flet framework. It simplifies application development by separating UI and logic while providing intuitive navigation solutions.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/saurabhwadekar/FletX",
    include_package_data=True,
    install_requires=[
        "repath",
        "flet",
    ],

)