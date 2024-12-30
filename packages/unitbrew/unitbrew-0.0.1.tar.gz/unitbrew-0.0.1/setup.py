from pathlib import Path
from setuptools import setup, find_packages


version_dict = {}
with open(Path(__file__).parents[0] / "unitbrew/_version.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["__version__"]
del version_dict


setup(
    name="unitbrew",
    version=version,
    author="Minwoo Kim",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/unitbrew",
    install_requies=[],
    packages=find_packages(),
    python_requires=">=3.10",
    package_data={"": ["*"]},
    install_requires=[],
    zip_safe=False,
)
