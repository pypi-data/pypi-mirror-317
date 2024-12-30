from setuptools import setup, find_packages

setup(
    name='Pysimxrd',
    version='0.1.1',
    description="XRD simulator",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # 明确指定 README 类型
    include_package_data=True,
    author='CaoBin',
    author_email='binjacobcao@gmail.com',
    maintainer='CaoBin',
    maintainer_email='binjacobcao@gmail.com',
    license='MIT License',
    url='https://github.com/Bin-Cao/SimXRD',
    packages=find_packages(),  # 自动包含所有 Python 模块
    package_data={
        'Pysimxrd': ['utils/*', 'CGCNN_atom_emb.json']  # 修复格式错误
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.5',
    install_requires=[
        'scipy',
        'ase',
        'pymatgen'
    ],  # 修复了列表中未使用引号的依赖项
    entry_points={
        'console_scripts': [
            # 如果需要定义 CLI 工具的入口点，可以在此处添加
        ],
    },
)
