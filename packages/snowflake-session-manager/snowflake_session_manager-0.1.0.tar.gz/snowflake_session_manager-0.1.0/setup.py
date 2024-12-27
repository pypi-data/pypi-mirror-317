from setuptools import setup, find_packages

setup(
    name="snowflake-session-manager",  # Replace with your package name
    version="0.1.0",                   # Update the version appropriately
    author="Your Name",                # Replace with your name
    author_email="your-email@example.com",  # Replace with your email
    packages=find_packages(),  # Automatically find all packages in the current directory
    install_requires=[
        "snowflake-snowpark-python",  # Snowflake Snowpark dependency
        "python-dotenv",              # To load .env files for environment variables
        "streamlit",                  # Streamlit dependency (if you're using it)
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Use your license if different
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # You can specify the Python version compatibility
    include_package_data=False,  # Do not include any additional files
)
