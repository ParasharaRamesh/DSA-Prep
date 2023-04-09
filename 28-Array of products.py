from functools import reduce

def arrayOfProducts(array):
    products = []
    for i in range(len(array)):
        #exclude i and get everything else
        filteredOutArray = array[:i] + array[i+1:]
        products.append(reduce(lambda x, y : x*y, filteredOutArray))
    return products

if __name__ == '__main__':
    array=[1,2,3,4]
    print(arrayOfProducts(array))