import os
import pymysql
import yaml
import pandas as pd


class Database:
    def __init__(self):
        CREDENTIAL_DIR = '.credentials'
        db_crediential = yaml.load(open(os.path.join(CREDENTIAL_DIR, 'db.yaml')), Loader=yaml.FullLoader)
        host = db_crediential['mysql_host']
        user = db_crediential['mysql_user']
        password = db_crediential['mysql_password']
        db = db_crediential['mysql_db']
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def insert_stock_data(self, filename):
        """
        SQL operation for inserting stock data into MySQL from a .csv file.
        """
        DATA_DIR = "./data"
        df = pd.read_csv(os.path.join(DATA_DIR, filename))

        for index, row in df.iterrows():
            self.cur.execute("INSERT INTO stockprice(ticker, date, open, high, low, close, volume) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                            (row['Ticker'], row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
            if index % 1000 == 0:
                print(f"Inserted {index} rows")
        self.con.commit()
        self.con.close()

    def select_stock_with_latest_info(self):
        """
        SQL operation for selecting stock data displayed in home page.
        """
        query = """
                    SELECT latest_price.Ticker, sector, country, Date, Open
                    FROM StockInfo INNER JOIN (
                        SELECT Ticker, Date, CAST(Open AS DECIMAL(5, 2)) AS Open
                        FROM StockPrice
                        WHERE Date = (SELECT MAX(Date)
                                    FROM StockPrice)) latest_price  ON latest_price.Ticker = StockInfo.Ticker          
                """  
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    def select_stock_with_max_price(self):
        """
        SQL operation for selecting stock data displayed in home page.
        """
        query = """
                    SELECT Ticker, MAX(Close)
                    FROM StockPrice
                    GROUP BY Ticker
                """  
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.cur.close()
        return result
    

    def select_stock_with_daily_price(self, ticker):
        query = f"""
                    SELECT Ticker, Date, CAST(Open AS DECIMAL(5, 2)) AS Open,
                                         CAST(High AS DECIMAL(5, 2)) AS High,
                                         CAST(Low AS DECIMAL(5, 2)) AS Low,
                                         CAST(Close AS DECIMAL(5, 2)) AS Close
                    FROM StockPrice
                    WHERE Ticker = '{str(ticker)}'
                 """  
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    def get_user_id(self, user_id):
        query = f"""
                    SELECT user_id
                    FROM Users
                    WHERE user_id = '{user_id}'
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result[0]['user_id']

    def get_user_password(self, user_id):
        query = f"""
                    SELECT password
                    FROM Users
                    WHERE user_id = '{user_id}'
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result[0]['password']

if __name__ == "__main__":
    # Test db connection
    db = Database()
    print(f"Connected: {db.con.open}")

    # Test
    # print(f"{db.select_stock_with_latest_info()[:2]}")
    # db.insert_stock_data("top500_Oct-09-2020.csv")
    # print(db.select_stock_with_max_price())
    # print(db.select_stock_with_daily_price('MSFT'))

    