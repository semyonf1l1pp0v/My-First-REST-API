import os

from datetime import datetime

from flask import Flask, jsonify, render_template
import sqlite3
from flask import request
from dotenv import load_dotenv

load_dotenv()

PATH_TO_DB = os.getenv("PATH_TO_DB_FILE")
PATH_TO_CSV = os.getenv("PATH_TO_CSV_FILE")

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def home():
    return render_template('home.html')


# Показать все записи
@app.route("/api/rows", methods=['GET'])
def rows_index():
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, latitude, longitude, emerg_title, emerg_timestamp, township FROM Emergency")
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)


# Показать запись
@app.route("/api/rows/<string:row_id>", methods=['GET'])
def rows_show(row_id):
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Emergency where rowid = ?", [row_id])
    data = cursor.fetchall()
    connection.close()
    return jsonify(data), 200


# Добавить запись
@app.route("/api/rows", methods=['POST'])
def rows_create():
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    emerg_title = request.form['emerg_title']
    emerg_timestamp = request.form['emerg_timestamp']
    township = request.form['township']

    cursor.execute("INSERT INTO Emergency VALUES (?,?,?,?,?)",
                   [latitude, longitude, emerg_title, emerg_timestamp, township])

    connection.commit()
    connection.close()
    return "New row created"


# Удалить запись
@app.route("/api/rows/<string:row_id>", methods=['DELETE'])
def rows_destroy(row_id):
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Emergency where rowid = ?", [row_id])
    if cursor.rowcount == 0:
        connection.close()
        return f"No row with ID {row_id}", 404
    connection.commit()
    connection.close()
    return f"Deleted row ID: {row_id}", 200


# Редактировать запись
@app.route("/api/rows/<int:row_id>", methods=['PUT'])
def rows_update(row_id):
    connection = sqlite3.connect(PATH_TO_DB)
    new_latitude = request.form['new_latitude']
    new_longitude = request.form['new_longitude']
    new_emerg_title = request.form['new_emerg_title']
    new_emerg_timestamp = request.form['new_emerg_timestamp']
    new_township = request.form['new_township']
    cursor = connection.cursor()

    cursor.execute(f"""UPDATE Emergency SET latitude = ?, longitude = ?, emerg_title = ?, emerg_timestamp = ?,
    township = ? where rowid = ?""",
                   [new_latitude, new_longitude, new_emerg_title, new_emerg_timestamp, new_township, row_id])

    connection.commit()
    connection.close()
    return f"Edited row ID: {row_id}"


# Показать число записей за конкретный час
@app.route("/api/hours/<string:hour>", methods=['GET'])
def hour_show(hour):
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()

    cursor.execute("""with t1 as(SELECT strftime('%H', emerg_timestamp) as hour,
    count(strftime('%H', emerg_timestamp)) as hour_count FROM Emergency group by 1)
    
    SELECT hour_count from t1 where hour = ?""", [hour])

    data = cursor.fetchall()
    connection.close()
    return data


@app.route('/api/rows/restore', methods=['GET'])
def rows_restore():
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS Emergency')
    connection.commit()

    # Создаем таблицу

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Emergency (
    latitude float,
    longitude float,
    emerg_title text,
    emerg_timestamp timestamp,
    township text
    )
    ''')

    connection.commit()

    # Загружаем данные из файла

    with open(PATH_TO_CSV, 'r') as file:
        for i, line in enumerate(file):
            if i == 10:
                break
            text = file.readline()
            attrs = text.split(',')
            if attrs[0] != '' and attrs[1] != '' and attrs[4] != '' and attrs[5] != '' and attrs[6] != '':
                timestamp = datetime.strptime(attrs[5], '%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    f'''INSERT INTO Emergency VALUES ({attrs[0]}, {attrs[1]}, "{attrs[4]}", "{timestamp}", "{attrs[6]}")''')
    connection.commit()
    connection.close()
    return render_template('home.html')
