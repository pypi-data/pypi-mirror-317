from setuptools import find_packages, setup

setup(
    name="pgliveapp",
    version="0.1.4",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="takumi-nishimura",
    author_email="clp13218@nitech.jp",
    url="https://github.com/takumi-nishimura/pgliveApp",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=["pglive>=0.8.0", "pyqt6>=6.8.0", "uv>=1.0.0"],
    entry_points={
        "console_scripts": [
            "pgliveapp=pgliveapp:main",
        ],
    },
)
