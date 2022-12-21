import csv
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p","--plot",
                        help="Show graph",
						action="store_true",
                        
                        )

    args = parser.parse_args()
    return(args)

def read_data(file_name):
    try :
        fd = open(file_name)
        reader = csv.reader(fd)
        data = list(reader)
    except PermissionError:
        print('Permission error')
        exit(0)
    except IsADirectoryError:
        print('Is a directory')
        exit(0)
    except FileNotFoundError:
        print('File not found')
        exit(0)
    except:
        print('Unknown error')
        exit(0)
    fd.close()
    return data

def check_data(data):
    if len(data) < 4:
        print('The data is not suffisent for a lineair regression')
        exit(0)
    for vector in data:
        if len(vector) != 2:
            print('file contains a non 2D line')
            exit(0)
        if len(vector[0]) == 0 or len(vector[1]) == 0:
            print('file contains an empty value')
            exit(0)

def clean_data(data):
    data.remove(data[0])
    i = 0
    clean_data = []
    while i < len(data):
        try:
            clean_data.append([float(data[i][0]), float(data[i][1])])
        except:
            print('Non numeric value')
            exit(0)
        i+= 1
    return clean_data

def get_min_max(data) :

    i = 0
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for vector in data:
        if vector[0] < min_x :
            min_x = vector[0]
        if vector[0] > max_x :
            max_x = vector[0]
        if vector[1] < min_y :
            min_y = vector[1]
        if vector[1] > max_y :
            max_y = vector[1]

    return {
            'max_x': max_x, 
            'max_y': max_y,
            'min_x': min_x,
            'min_y': min_y,
            }    

def get_unit_data(data, max_min) :

    unit_data = []

    diff_x = max_min['max_x'] - max_min['min_x']
    diff_y = max_min['max_y'] - max_min['min_y']
    if diff_x == 0 or diff_y == 0:
        return data
    
    for vector in data:
        unit_data.append(
            [(vector[0] - max_min['min_x']) / (max_min['max_x'] - max_min['min_x']),
             (vector[1] - max_min['min_y']) / (max_min['max_y'] - max_min['min_y'])]
        )
    return unit_data

def estimatePrice(value, theta_0, theta_1) :
        return theta_0 + theta_1 * value
        

def mean_square_error(data, theta_0, theta_1):
    summ = 0

    for vector in data:
        tmp_diff = estimatePrice(vector[0], theta_0, theta_1) - vector[1]
        tmp_diff *= tmp_diff
        summ += tmp_diff

    return summ / len(data)


def get_gradient0(data, theta_0, theta_1):
    summ = 0.0

    for vector in data:
        summ += estimatePrice(vector[0], theta_0, theta_1) - vector[1]
        
    return (summ / len(data))


def get_gradient1(data, theta_0, theta_1):
    summ = 0.0

    for vector in data:
        summ += (estimatePrice(vector[0], theta_0, theta_1) - vector[1]) * vector[0]
    return (summ / len(data))

def save_thetas(theta_0, theta_1):
    f = open("thetas.csv", "w+")
    f.write('theta_0, theta_1\n')
    f.write("%f, %f" %(theta_0, theta_1))
    f.close()

def train(data, min_max):
    learning_rate = 0.01
    theta_1 = 0.0
    tmp_theta_0 = 1.0
    tmp_theta_1 = 1.0
    prev_mse = 0.0
    cur_mse = mean_square_error(data, tmp_theta_0, tmp_theta_1)
    delta_mse = cur_mse

    while delta_mse > 0.0000001 or delta_mse < -0.0000001:
        theta_0 = tmp_theta_0
        theta_1 = tmp_theta_1
        tmp0 = learning_rate * get_gradient0(data, tmp_theta_0, tmp_theta_1)
        tmp_theta_1 -= learning_rate * get_gradient1(data, tmp_theta_0, tmp_theta_1)
        tmp_theta_0 -= tmp0
        prev_mse = cur_mse
        cur_mse = mean_square_error(data, tmp_theta_0, tmp_theta_1)
        delta_mse = cur_mse - prev_mse

    theta_1 = (min_max['max_y'] - min_max['min_y']) * theta_1 / (min_max['max_x'] - min_max['min_x'])
    theta_0 = min_max['min_y'] + ((min_max['max_y'] - min_max['min_y']) * theta_0) + theta_1 * (1 - min_max['min_x'])
    save_thetas(theta_0, theta_1)
    return {
        'theta_0': theta_0,
        'theta_1': theta_1,
    }

if __name__ == '__main__':
    data = read_data('data.csv')
    check_data(data)
    data = clean_data(data)
    limits = get_min_max(data)
    unit = get_unit_data(data, limits)
    thetas = train(unit, limits)

    args = parse_args()
    if args.plot == True:
        to_plot = [[], []]
        for vector in data:
            to_plot[0].append(vector[0])
            to_plot[1].append(vector[1])
        vector_1 = [limits['min_x'], limits['max_x']]
        vector_2 = [thetas['theta_0'] + thetas['theta_1'] * limits['min_x'], \
			thetas['theta_0'] + thetas['theta_1'] * limits['max_x']]
        fig = plt.figure()
        plt.xlabel('Km')
        plt.ylabel('Price')
        plt.plot(to_plot[0], to_plot[1], 'ro')
        plt.plot([limits['min_x'], limits['max_x']],\
			 [thetas['theta_0'] + thetas['theta_1'] * limits['min_x'], \
				thetas['theta_0'] + thetas['theta_1'] * limits['max_x']])
        plt.show()
    
