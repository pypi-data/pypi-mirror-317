from setuptools import setup, find_packages

setup(
    name="lilliepy bling", 
    package=['lilliepy_bling'], 
    version="1.0.0",  
    author="sarthak ghoshal",  
    author_email="sarthak22.ghoshal@gmail.com",  
    description="a function to run code on a server, away from the client",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    url="https://github.com/websitedeb/lilliepy_server",  
    packages=find_packages(),
    keywords=["lilliepy server component", "lilliepy", "reactpy", "lilliepy bling"],
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.0.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    license="MIT",
)
