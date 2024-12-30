from setuptools import setup, find_packages

setup(
    name='AndroidTraceTool',  # 模块名称
    version='0.1.1',  # 版本号
    packages=find_packages(),  # 自动查找所有包
    python_requires='>=3.7',  # 支持的Python版本
    author='shersty',  # 作者信息
    author_email='2237321879@qq.com',
    description='A tool that support add trace by python code!',  # 简短描述
    long_description=open('AndroidTraceTool/README.md', 'r').read(),  # 长描述（通常读取自README文件）
    long_description_content_type='text/markdown',  # 长描述类型
    include_package_data=True,
    package_data={
        '': ['*.dex', '*.md'],  # dex和md
    },
    url='',  # 项目主页
    classifiers=[  # 项目分类标签
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
