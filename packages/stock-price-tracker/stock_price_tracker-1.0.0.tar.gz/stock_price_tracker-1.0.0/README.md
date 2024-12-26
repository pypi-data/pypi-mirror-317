# Stock Price Tracker

The **Stock Price Tracker** is a Python package that allows you to monitor stock prices and receive email alerts when a stock's price meets a specified target. This package uses `yfinance` to fetch real-time stock data, `apscheduler` for scheduling periodic checks, and `smtplib` to send email notifications.

---

## Features

- Add multiple stocks to monitor with desired price thresholds.
- Send email notifications when a stock's price falls below the specified target.
- Schedule stock price checks with a default interval of 15 hours.
- Flexible and customizable scheduling.

---

## Installation

To install the package, run:

```bash
pip install stock_price_tracker
```

---

## Usage

### 1. Import the package and initialize the tracker

```python
from stock_price_tracker import StockPriceTracker

tracker = StockPriceTracker(
    smtp_server="appropriate_server",
    smtp_port=(port_number),
    email="your_email@gmail.com",
    password="your_email_password",
    recipient_email="recipient_email@gmail.com"
)
```

### 2. Add stocks to monitor

```python
tracker.add_stock("AAPL", 150)  # Apple stock, target price: $150
tracker.add_stock("GOOGL", 2500)  # Alphabet stock, target price: $2500
```

### 3. Start the scheduler

```python
tracker.start_scheduler()
```

The scheduler will run checks every 15 hours by default.

---

## Example

```python
from stock_price_tracker import StockPriceTracker

# Initialize the tracker
tracker = StockPriceTracker(
    smtp_server="smtp.gmail.com",  # Use the appropriate SMTP server
    smtp_port=587,  # Port for Gmail
    email="your_email@gmail.com",  # Your email address
    password="your_email_password",  # Your email app-specific password
    recipient_email="recipient_email@gmail.com"  # Email to receive alerts
)

# Add stocks
tracker.add_stock("AAPL", 150)
tracker.add_stock("MSFT", 280)

# Check prices immediately
tracker.check_prices()

# Start monitoring
tracker.start_scheduler()
```

---

## Requirements

- Python >= 3.6
- Dependencies:
  - `yfinance`
  - `apscheduler`

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

---

## Contact

For questions or feedback, you can reach me at [GitHub Profile](https://github.com/Vaishaliyadavv).
