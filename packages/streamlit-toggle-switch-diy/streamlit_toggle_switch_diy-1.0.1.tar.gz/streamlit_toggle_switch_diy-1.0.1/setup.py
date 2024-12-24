import setuptools

setuptools.setup(
    name="streamlit_toggle_switch_diy",
    version="1.0.1",
    author="Flow_Water",
    author_email="1665526933@qq.com",
    description="Creates a customizable toggle, and you can switch the background color of label",
    url="https://github.com/sqlinsights/streamlit-toggle-switch",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
