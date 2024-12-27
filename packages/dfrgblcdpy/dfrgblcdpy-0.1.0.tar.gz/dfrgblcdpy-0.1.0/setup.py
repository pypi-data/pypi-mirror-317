from setuptools import setup

with open("requirements.txt") as f:
    REQUIRES = f.readlines()

with open("test-requirements.txt") as f:
    TESTS_REQUIRES = f.readlines()

setup(
    name="dfrgblcdpy",
    version="0.1.0",
    description="Python library to control DFRobot Gravity I2C LCD1602 with RGB Backlight Display",
    author_email="tomasz.prus@gmail.com",
    author="Tomasz Prus",
    license="MIT License",
    url="https://github.com/tomplus/DFRGBLCDpy",
    keywords=["Raspberry", "LCD", "RGB", "DFRobot"],
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
    packages=["dfrgblcdpy"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
