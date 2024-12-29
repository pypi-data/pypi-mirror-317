from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='streamlit_custome_css',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'streamlit',
    ],  # Add a comma here
    author='leo joel roys',
    author_email='joelroys637@gmail.com',
    description='streamlit custome css function and sending mail services , text to speech ',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
     project_urls={
           'Source Repository': 'https://github.com/Joelroys637' #replace with your github source
    }
)
