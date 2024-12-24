import setuptools

setuptools.setup(
    name="streamlit_toggle_switch_diy",
    version="1.0.2",
    author="Flow Water",
    author_email="1665526933@qq.com",
    description="Creates a customizable toggle, and you can change the label's background-color.",

    long_description_content_type="text/plain",
    url="https://github.com/sqlinsights/streamlit-toggle-switch",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
