from setuptools import find_packages, setup

setup(name="islucky",  # 包名称
      version="0.1.0",  # 版本号
      author="yuanze31",  # 作者名
      author_email="yuanze31@yuanze31.com",  # 作者邮箱
      description="Today is lucky or not?",  # 简单描述
      packages=find_packages(),  # 自动发现子模块
      python_requires=">=3.6",  # 需要的 Python 版本
      )
