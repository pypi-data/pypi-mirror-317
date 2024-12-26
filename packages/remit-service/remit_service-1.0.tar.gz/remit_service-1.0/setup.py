from setuptools import setup, find_packages


setup(
    name="remit_service",
    version="1.0",
    packages=find_packages(
        include=[
            "remin_service", "remin_service.*"
        ]
        # exclude=[
        #     "src",
        # ]
    ),
    package_data={
        'remin_service': ['static/**'],  # 包含所有 .py 文件
    },
    install_requires=[
        "fastapi==0.115.6",
        "uvicorn==0.34.0",
        "loguru==0.7.3",
        "PyYAML==6.0.2",
        "PyYAML==6.0.2",
        "python-nacos==0.1.1"
    ],
    python_requires=">=3.10",
    include_package_data=True
)