from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()
HY = "-e ."
def get_requirements(file_path):
    requirements = []
    with open(file_path ) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if HY in requirements:
            requirements.remove(HY)
    return requirements
         
         # Call the setup function to define package metadata
setup(
    name="ml-packages",  # Replace with your package name
    version="1.0",  # Start with a version number
    author="kamal",  # Your name or organization
    author_email="kamalar710@gmail.com",  # Your email address
    description="A package for Logistic Regression, KNN, and Decision Linear SVM",
    long_description=long_description,  # Read from the README file
    long_description_content_type="text/markdown",  # Specifies markdown format
    url="https://github.com/kam-999/ml-packages.git",  # Package repository URL
    packages=find_packages(),  # Automatically finds all packages in the directory
    
    install_requires=get_requirements("requirements.txt")
   
)
