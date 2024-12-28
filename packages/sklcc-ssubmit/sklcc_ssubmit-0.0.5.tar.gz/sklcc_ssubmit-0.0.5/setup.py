import setuptools

setuptools.setup(
    name="sklcc_ssubmit",
    version="0.0.5",
    packages=setuptools.find_packages(),
    install_requires=['bcrypt>=4.0.1','cffi>=1.15.1','cryptography>=40.0.2','paramiko>=3.5.0','pycparser>=2.21','PyNaCl>=1.5.0'],
    python_requires=">=3.6"

)