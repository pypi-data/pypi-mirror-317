from setuptools import setup

setup(
    name="NeuralRF",
    version="0.1.0",
    long_description="NeuralRF",
    long_description_content_type="text/markdown",
    packages=["neuralrf"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
