from macd_calculate import *
from mysql import *
from multprocess_stock import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # main()
    ind = 'sz'
    rl = macd(select_index(ind))
    fig = plt.figure()
    fig.suptitle(ind, fontsize=20)
    ax1 = fig.add_subplot(1, 1, 1)
    data_list1 = list()
    data_list2 = list()
    index_list = rl.index_list
    #data_list3 = list()
    for i in xrange(0, len(index_list)):
        data_list1.append(rl.dicDIF[index_list[i]])
        data_list2.append(rl.dicEDA[index_list[i]])
        # data_list3.append(dicBAR[index_list[i]])
    # ax1.plot(np.arange(100) * 0)
    n = len(index_list)
    ax1.plot(data_list1[0:n], color='g')
    ax1.plot(data_list2[0:n], color='r')
    # ax1.bar(np.arange(len(data_list3[0:n])),
    #        data_list3[0:n], alpha=0.1, color="blue")
    # ax1.set_xticklabels(index_list, rotation=30, fontsize='small')
    # ax1.hist([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]*3, bins=50,
    #         normed = 1, facecolor = 'blue', alpha = 1)
    plt.show()
