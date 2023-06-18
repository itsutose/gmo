def weighted_ave(pairs):
    # data = [1, 2, 3, 4, 5]  # データ
    # weights = [0.1, 0.2, 0.3, 0.2, 0.2]  # 重み

    # 各データと重みを掛け合わせた値の総和を求める

    weighted_sum = sum([pair[0]*pair[1] for pair in pairs])

    # 重みの総和を求める
    weights_sum = sum([pair[0] for pair in pairs])


    # 加重平均を求める
    weighted_avg = weighted_sum / weights_sum

    print(weights_sum, weighted_avg)

    print("加重平均：", weighted_sum)

if __name__ == '__main__':
    pairs = [[0.0002, 3991900], [0.0002, 3990000], [0.0001, 3998400], [0.0001, 4000000]]
    weighted_ave(pairs)