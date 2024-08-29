import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zoltraakklein",
    version="1.0.5",
    author="Daisuke Yamaguchi",
    author_email="daicom0204@gmail.com",
    description="Simplified class for Zoltraak, a digital content production framework by working with LLMs and generative AIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/zoltraakklein/",
    project_urls={
        'Homepage': 'https://habatakurikei.com/',
        'GitHub': 'https://github.com/Habatakurikei/zoltraakklein',
    },
    packages=setuptools.find_packages(),
    package_data={
        'zoltraakklein': ['architect/*','compilers/*', 'instructions/*', 'prompts/*', 'rosetta/*', 'templates/**/*'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "llmmaster>=0.3.4",
        "opencv-python>=4.10.0.84",
        "moviepy>=1.0.3",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=6.0",
        ],
    },
)
