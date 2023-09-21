import psycopg2
import requests
import pandas as pd
import matplotlib.pyplot as plt

from config import host, port, user, password, db_name
from config import bot_token, chat_id


def connect_to_database():
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM avg_view")
            data = cursor.fetchone()
            if data:
                data = list(data)
                columns = ['Week', 'Month', '3 Months', 'Average']
                df = pd.DataFrame([data], columns=columns)
                df = df.apply(lambda x: x.astype(float))
                return df
            else:
                return None
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


def calculate_averages(df):
    weekly_avg = df['Week'].mean()
    monthly_avg = df['Month'].mean()
    three_months_avg = df['3 Months'].mean()

    df.plot(kind='bar', rot=0, title='Average Values', legend=False)
    plt.xlabel('Period')
    plt.ylabel('Average')
    plt.savefig('average_values.png')
    plt.close()


def send_plot_to_telegram(image_path):
    try:
        url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("Plot sent to Telegram successfully.")
        else:
            print("Failed to send plot to Telegram.")
    except Exception as e:
        print("Error sending plot to Telegram:", e)


def main():
    df = connect_to_database()

    if df is not None:
        calculate_averages(df)
        send_plot_to_telegram('average_values.png')
    else:
        print("No data found in the database.")


if __name__ == "__main__":
    main()
