import unittest
from datetime import datetime


class Stock:
    def __init__(self, symbol, prices):
        self.symbol = symbol
        self.prices = prices  # Dictionary with dates as keys and prices as values

    def Price(self, date):
        """Returns the price of the stock on a specific date."""
        date = datetime.strptime(date, "%Y-%m-%d")
        for d in sorted(self.prices.keys()):
            if datetime.strptime(d, "%Y-%m-%d") <= date:
                price = self.prices[d]
        return price


class Portfolio:
    def __init__(self):
        self.stocks = []

    def add_stock(self, stock):
        """Adds a Stock object to the portfolio."""
        self.stocks.append(stock)

    def Profit(self, start_date, end_date):
        """Calculates the portfolio's profit between two dates."""
        start_value = 0
        end_value = 0
        for stock in self.stocks:
            start_value += stock.Price(start_date)
            end_value += stock.Price(end_date)
        return end_value - start_value

    def AnnualizedReturn(self, start_date, end_date):
        """Calculates the annualized return of the portfolio."""
        start_value = 0
        end_value = 0
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        years = (end_datetime - start_datetime).days / 365.0

        for stock in self.stocks:
            start_value += stock.Price(start_date)
            end_value += stock.Price(end_date)

        if start_value == 0:
            return 0
        total_return = (end_value / start_value) - 1
        annualized_return = (1 + total_return) ** (1 / years) - 1
        return annualized_return

# Unit Test Class


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        """Sets up a sample portfolio for testing."""
        self.apple = Stock("AAPL", {
            "2023-01-01": 150,
            "2024-01-01": 175
        })
        self.google = Stock("GOOG", {
            "2023-01-01": 2800,
            "2024-01-01": 3000
        })
        self.portfolio = Portfolio()
        self.portfolio.add_stock(self.apple)
        self.portfolio.add_stock(self.google)

    def test_profit(self):
        """Tests the profit calculation."""
        profit = self.portfolio.Profit("2023-01-01", "2024-01-01")
        self.assertEqual(profit, (175 - 150) + (3000 - 2800))

    def test_annualized_return(self):
        """Tests the annualized return calculation."""
        annualized_return = self.portfolio.AnnualizedReturn(
            "2023-01-01", "2024-01-01")
        expected_return = (
            ((1 + (175 - 150) / 150) + (1 + (3000 - 2800) / 2800)) / 2) ** (1 / 1) - 1
        self.assertAlmostEqual(annualized_return, expected_return, places=4)

    def test_empty_portfolio(self):
        """Tests the case where the portfolio has no stocks."""
        empty_portfolio = Portfolio()
        profit = empty_portfolio.Profit("2023-01-01", "2024-01-01")
        self.assertEqual(profit, 0)
        annualized_return = empty_portfolio.AnnualizedReturn(
            "2023-01-01", "2024-01-01")
        self.assertEqual(annualized_return, 0)


if __name__ == "__main__":
    unittest.main()
