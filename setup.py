from setuptools import setup

setup(
    name="rss2cube",
    version="0.1",
    description="Convert MEGARA RSS spectra to 3d fits datacube",
    url="https://github.com/PsyJim/rss2cube",
    author="Jim Acosta",
    author_email="jg.acostaangulo@ugto.mx",
    license="GNU GPL-3",
    packages=["rss2cube"],
    install_requires=["setuptools", "numpy", "astropy", "scipy", "megaradrp"],
    zip_safe=False,
)
