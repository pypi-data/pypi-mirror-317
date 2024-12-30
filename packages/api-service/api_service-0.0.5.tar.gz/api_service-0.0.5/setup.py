from setuptools import setup, find_packages


# Read long description from file README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="api_service",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.103.1",
        "python-decouple>=3.8",
        "bcrypt>=4.0.1",
        "pydantic[email]>=2.4.2",
    ],
    author="Alfonso Falcone",
    description="""This library will create and validate JWT tokens
        and decode and validate queries against a pydantic model in input.
        In order to work succesfully, it needs that you have defined 
        the following environment variables: 'JWT_SECRET' your secret key
        for generating tokens,'JWT_ALGORITHM' your favorite algorithm to be
        use to generate the tokens""",
    keywords=["fastapi", "bcrypt", "jwt", "pydantic"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
