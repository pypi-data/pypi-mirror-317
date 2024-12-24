import setuptools

"""
with open('./Agently/requirements.txt') as f:
    origin_requirements = f.read().splitlines()

requirements = []
for requirement in origin_requirements:
    if not requirement.startswith("#"):
        requirements.append(requirement)
"""
        
setuptools.setup(
    name = "agently-stage",
    version = "0.1.1",
    author = "Maplemx, AgentEra Ltd. Agently Team",
    author_email = "moxin@agently.tech",
    description = "Agently Stage makes multi-threads & async tasks management easier!",
    long_description = "Agently Stage create an instance to manage multi-threads and async tasks in its dispatch environment. Agently Stage dispatch environment will allow tasks managed by this Agently Stage instance to be run in an independent thread with an independent async event loop that will not disturb other tasks create or managed by other Agently Stage instance, other packages or other complex async/multi-threading logic.Agently Stage also includes tools like Agently Stage EventEmitter and Agently Stage Tunnel. They are also very useful when coding with multi-threads and async.",
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
