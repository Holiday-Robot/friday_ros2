from glob import glob

from setuptools import find_packages, setup

package_name = "friday_manipulation"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", glob("package.xml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Holiday Robotics Open Source",
    maintainer_email="opensource@holiday-robotics.com",
    description="One-shot manipulation command examples for Friday.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "cartesian_space = friday_manipulation.cartesian_space:main",
            "joint_space = friday_manipulation.joint_space:main",
        ],
    },
)
