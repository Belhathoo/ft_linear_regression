import argparse
import csv

from learn import read_data, estimatePrice, clean_data

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-km","--Kilometers",
                        help="Number of kilometers",
                        
                        type=float,
                        
                        )

    args = parser.parse_args()
    return(args)

def check_data(data):
    if len(thetas) < 2:
        print(0)
        exit(1)
    if len(data) != 2:
        print('Multiple data lines')
        exit(0)
    vector = data[1]
    if len(vector) != 2:
        print('Non 2D line')
        exit(0)
    if len(vector[0]) == 0 or len(vector[1]) == 0:
        print('Empty value')
        exit(0)

if __name__ == '__main__':

    args = parse_args()

    #initialise sender and receiver country
    km = args.Kilometers

    thetas = read_data('./thetas.csv')
    check_data(thetas)
    thetas = clean_data(thetas)
    
    print(estimatePrice(km, thetas[0][0], thetas[0][1]))
    