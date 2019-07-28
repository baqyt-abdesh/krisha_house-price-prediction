import pandas as pd
import numpy as np

file = 'krisha.csv'

df = pd.read_csv(file)

# print(df.head())



df = df.iloc[:, :4]
# print(df.head())

x = []
y = []

for i in range(len(df)):
    sel = df.iloc[i]
    x.append([1, float(sel['rooms']), float(sel['area']), float(sel['year'])])
    y.append(float(sel['price']))

x_num = np.array(x)
y_num = np.array(y)


'''
x - xmin
xmax - xmin
'''



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


alpha = 0.1
m = len(x_num)


thetas = np.random.rand(1, 4)
y_num.shape = (y_num.shape[0], 1)
thetas = thetas.T





for i in range(5000):
    h = np.dot(x_num, thetas)
    j = 1 / m * np.dot(x_num.T, (h - y_num))
    thetas = thetas - alpha * j





my_rooms = float(input('rooms: '))
my_area = float(input('area: '))
my_year = float(input('year: '))
my_inp = np.array([1, (my_rooms - x_min_rooms) / (x_max_rooms - x_min_rooms), (my_area - x_min_area) / (x_max_area - x_min_area), (my_year - x_min_year) / (x_max_year - x_min_year)])


y_norm = (np.dot(thetas.T, my_inp))

out = y_norm * y_max - y_norm * y_min + y_min
print(out)

