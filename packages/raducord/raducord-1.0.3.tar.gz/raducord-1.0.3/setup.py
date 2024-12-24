from setuptools import setup, find_packages

VERSION = "1.0.3"

setup(
    name="raducord",
    version=VERSION,
    author="H4cK3dR4Du",
    author_email="<rostermast70@gmail.com>",
    url="https://github.com/H4cK3dR4Du/raducord",
    description="The best library for designs, with a wide variety of colors and useful utils for your tools.",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "tls_client",
        "fake_useragent",
        "windows-curses; platform_system=='Windows'",
        "pyfiglet",
        "typing_extensions"
    ],
    keywords=["python", "utils", "color", "colors", "tools"],
    python_requires=">=3.8.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
