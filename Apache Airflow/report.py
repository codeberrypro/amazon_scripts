import requests
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from config import host, port, user, password, db_name
from config import bot_token, chat_id
from datetime import datetime, timedelta


default_args = {
    'owner': 'ваше_имя',
    'start_date': datetime(2023, 1, 1, 8, 0),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'send_plot_to_telegram',
    default_args=default_args,
    schedule_interval='0 8 * * 1',
    catchup=False,
)


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
    x_values = ['Weekly Avg', 'Monthly Avg', '3 Months Avg']
    averages = [df['Week'].mean(), df['Month'].mean(), df['3 Months'].mean()]

    plt.bar(x_values, averages, color='blue')
    plt.title('Average Values in hours')
    plt.xlabel('Time Period')
    plt.ylabel('Average')
    plt.savefig('average_values.png')
    plt.close()


def send_plot_to_telegram():
    try:
        image_path = 'average_values.png'
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
        send_plot_to_telegram()
    else:
        print("No data found in the database.")


if __name__ == "__main__":
    main()
