from setuptools import setup, find_packages

# Read long description from the README.md file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="anticp3",  # Replace with your package name
    version="1.0",  # Initial version
    author="Amisha Gupta",
    author_email="amisha23225@iiitd.ac.in",
    description="AntiCP3 : Prediction of Anticancer Proteins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amisha1699/anticp3",  # Replace with your repo URL if hosting
    packages=find_packages(),  # Automatically finds submodules
    include_package_data=True,  # Includes files in MANIFEST.in
    install_requires=install_requires,  # Dependencies
    entry_points={  # Entry point for the command line tool
        "console_scripts": [
            "anticp3=anticp3:run",  # Runs anticp3.py's main code block
        ],
    },
)
