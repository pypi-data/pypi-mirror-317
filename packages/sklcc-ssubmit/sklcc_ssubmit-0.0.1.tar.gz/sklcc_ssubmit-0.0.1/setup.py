import setuptools

setuptools.setup(
    name="sklcc_ssubmit",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=['bcrypt>=4.2.1','cffi>=1.17.1','cryptography>=44.0.0','paramiko>=3.5.0','pycparser>=2.22','PyNaCl>=1.5.0'],
    python_requires=">=3.6"

)