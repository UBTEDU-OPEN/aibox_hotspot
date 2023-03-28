from setuptools import setup, find_namespace_packages

setup(
    name = "hotspot",
    version = "0.1.0",
    description = "hotspot",
    long_description = "",

    packages = find_namespace_packages(include=["hotspot","hotspot.*"]),
    package_data = {"hotspot": ["*"],
                    "hotspot.assets": ["*"],
                    "hotspot.common": ["*"],
                    "hotspot.common.config": ["*"],
                    "hotspot.common.utils": ["*"],
                    },
    include_package_data = True,
    platforms = "any",
)
