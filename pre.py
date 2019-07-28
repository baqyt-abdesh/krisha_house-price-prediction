import pandas as pd
import numpy as np
from flask import Flask, render_template, request

file = 'krisha.csv'

df = pd.read_csv(file)

df = df.iloc[:, :4]

x = []
y = []

for i in range(len(df)):
    sel = df.iloc[i]
    x.append([1, float(sel['rooms']), float(sel['area']), float(sel['year'])])
    y.append(float(sel['price']))

x_num = np.array(x)
y_num = np.array(y)

max_rooms = np.max(x_num[:, 0])
min_rooms = np.min(x_num[:, 0])

# print(x_num.shape[1])
x_max_rooms = np.max(x_num[:, 1])
x_max_area = np.max(x_num[:, 2])
x_max_year = np.max(x_num[:, 3])
x_min_rooms = np.min(x_num[:, 1])
x_min_area = np.min(x_num[:, 2])
x_min_year = np.min(x_num[:, 3])
y_min = np.min(y[:])
y_max = np.max(y[:])
#normalize
y_num[:] = (y_num[:] - np.min(y_num[:])) / (np.max(y_num[:]) - np.min(y_num[:]))
for i in range(1, x_num.shape[1]):
    x_num[:, i] = (x_num[:, i] - np.min(x_num[:, i])) / (np.max(x_num[:, i]) - np.min(x_num[:, i]))

alpha = 0.01
m = len(x_num)

thetas = np.random.rand(1, 4)
y_num.shape = (y_num.shape[0], 1)
thetas = thetas.T

for i in range(5000):
    h = np.dot(x_num, thetas)
    j = 1 / m * np.dot(x_num.T, (h - y_num))
    thetas = thetas - alpha * j

app = Flask(__name__)

@app.route('/')
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        rooms = float(request.form['rooms'])
        area = float(request.form['area'])
        year = float(request.form['year'])
        rooms_norm = (rooms - x_min_rooms) / (x_max_rooms - x_min_rooms)
        area_norm = (area - x_min_area) / (x_max_area - x_min_area)
        year_norm = (year - x_min_year) / (x_max_year - x_min_year)
        inputs = np.array([1.0, rooms_norm, area_norm, year_norm])
        inputs.shape = (4, 1)
        mul = np.dot(thetas.T, inputs)
        out = mul * y_max - mul * y_min + y_min
        out = int(out[0])
        mini = int(out * 0.9)
        maxi = int(out * 1.1)
        return render_template('result.html', mini=mini, maxi=maxi)
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run(debug=True, port=7070)