import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="sjtools", 
    version="0.0.4a", 
    author="DEV|SJ", 
    author_email="sijeydev@gmail.com", 
    packages=["sjtools"], 
    description="My test package", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://t.me/sijeydev", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=['requests>=2.25.1'] 
) 
