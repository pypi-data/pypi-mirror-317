from setuptools import setup, find_packages

setup(
    name="stock_price_tracker",
    version="1.0.0",
    author="Vaishali Yadav",
    description="A Python package to track stock prices and send email alerts when price conditions are met.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vaishaliyadavv/stock_price_tracker.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "yfinance",
        "apscheduler",
    ],
    entry_points={
        "console_scripts": [
            # Directly referencing the class
            "stock-price-tracker=stock_price_tracker.tracker:StockPriceTracker",
        ],
    },

)
