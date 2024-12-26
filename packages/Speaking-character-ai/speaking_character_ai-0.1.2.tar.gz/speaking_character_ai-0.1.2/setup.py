from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="Speaking-character-ai",
    version="0.1.2",
    author="Speaking Character AI",
    author_email="contact@speakingcharacter.ai",
    description="A Speaking Character AI is a Python library designed to create virtual characters capable of engaging in interactive conversations. It can synthesize speech, generate text-based dialogue, and animate expressions or gestures in response to user inputs, enhancing the user experience in applications such as games, virtual assistants, and storytelling platforms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://speakingcharacter.ai/",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "speaking-character-ai=speaking_character_ai.app:run_app",
        ],
    },
) 