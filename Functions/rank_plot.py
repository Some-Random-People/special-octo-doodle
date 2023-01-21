import matplotlib.pyplot as plt

def plots(y):
    x = []
    for i in range(1,91):
        x.append(i)
    y.reverse()
    plt.plot(x, y)
    plt.xlabel("")
    plt.ylabel("")
    plt.title("")
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.ticklabel_format(style='plain')
    plt.savefig("./Temp/plot.png")
    plt.clf()
