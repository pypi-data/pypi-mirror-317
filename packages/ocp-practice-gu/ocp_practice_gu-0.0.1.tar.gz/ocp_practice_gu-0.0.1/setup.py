import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocp-practice-gu",
    version="0.0.1",
    author="Geun Ho Gu",
    author_email="googhgoo@hotmail.com",
    description="Quick start for ocp-catalysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuGroup/ocp-practice-gu",
    packages=['ocp_practice_gu'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)