import matplotlib.pyplot as plt

def plots(y):
    x = []
    for i in range(90,0,-1):
        x.append(i)
    plt.plot(x, y)
    plt.xlabel("")
    plt.ylabel("")
    plt.title("")
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.ticklabel_format(style='plain')
    plt.savefig("./Temp/plot.png")
    plt.clf()
