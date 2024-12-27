from setuptools import setup, find_packages
import os

# Define paths for frontend build files
frontend_path = os.path.join('streamlit_chat_widget', 'frontend', 'build')

setup(
    name="streamlit_chat_widget_tiangong",
    version="0.0.3",
    description="A custom chat input widget for Streamlit based on Mohammed Bahageel's Chat Input Widget project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nan LI",
    author_email="linanenv@gmail.com",
    url="https://github.com/linancn/Chat_input_widget",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",  # Include other dependencies if needed
    ],
    package_data={
        "streamlit_chat_widget_tiangong": ["frontend/build/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
