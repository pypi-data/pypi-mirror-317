import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugin-furrybar",
    version="1.6.0",
    author="huilongxiji",
    author_email="2601515849@qq.com",
    description="FurryBar插件",
    license='GPL-3.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huilongxiji/nonebot-plugin-furrybar",
    packages=setuptools.find_packages(),
    install_requires=['nonebot2>=2.2.1', 'httpx>=0.27.0', 'nonebot-adapter-onebot>=2.4.3'],
    python_requires='>=3.9',
)