#!/usr/bin/env python
import setuptools

setuptools.setup(
    setup_requires=['d2to2'],
    d2to1=True,
    test_suite='nose.collector',
    package_data={"velo": [
        "templates/*.*",
        "templates/*/*.*",
        "static/*.*",
        "static/*/*.*",
        "static/*/*/*.*",
    ]},
    entry_points="""\
        [paste.app_factory]
            main = velo:main
    """
    )
