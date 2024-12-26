import setuptools

"""
with open('./Agently/requirements.txt') as f:
    origin_requirements = f.read().splitlines()

requirements = []
for requirement in origin_requirements:
    if not requirement.startswith("#"):
        requirements.append(requirement)
"""
with open('./README.md') as f:
    long_description=f.read()
        
setuptools.setup(
    name = "agently_stage",
    version = "0.1.3",
    author = "Maplemx, AgentEra Ltd. Agently Team",
    author_email = "moxin@agently.tech",
    description = "Agently Stage - Efficient Convenient Asynchronous and Multithreaded Programming",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/AgentEra/agently-stage",
    license='Apache License, Version 2.0',
    packages = setuptools.find_packages(),
    #package_data = {"": ["*.txt", "*.ini"]},
    #install_requires= requirements,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
