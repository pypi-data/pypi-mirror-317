from setuptools import setup, find_packages

# Read the content of your README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="streamlit-mui-elements",
    version="0.0.18",
    author="Tom Jose",
    author_email="tomj0311@gmail.com",
    description="A Streamlit component for Material-UI elements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/streamlit-mui-elements",  # Update with your repository URL
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    data_files=[
        ('streamlit_mui_elements/frontend/build', [
            'streamlit_mui_elements/frontend/build/index.html',
            'streamlit_mui_elements/frontend/build/asset-manifest.json'
        ]),
    ],
    package_data={
        'streamlit_mui_elements': [
            'frontend/build/*',
            'frontend/build/**/*',
            'frontend/build/static/**/*',
            'frontend/build/static/css/*',
            'frontend/build/static/js/*',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",  # Set to Apache 2.0
        "Operating System :: OS Independent",
    ],
    license="Apache 2.0",  # Specify the license explicitly
    python_requires=">=3.6",
    install_requires=[
        "streamlit>=1.0.0",
    ],
    extras_require={
        "devel": [
            "wheel",
        ]
    }
)
