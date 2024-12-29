from setuptools import setup

setup(
    name="steamlibrary_publisher_percentage",  # The name of your package
    version="1.0",  # Update this for new versions
    py_modules=["steam-exporter"],  # Your Python script without the .py extension
    description="A Python package to calculate publisher percentages for Steam libraries",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hamburgerghini1/steamlibrary_publisher-percentage",
    author="Tommi Pöntinen",
    author_email="tommipontinen76@proton.me",
    license="MIT",  # Or the license you're using
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
    include_package_data=True,  # Include additional files specified in MANIFEST.in
)
