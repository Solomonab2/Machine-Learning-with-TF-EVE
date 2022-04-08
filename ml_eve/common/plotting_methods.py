""" various methods for plotting figures of TensorFlow model data """

from matplotlib import pyplot as plt


def plot_metrics(epochs, hist, list_of_metrics):
    """Plot a curve of one or more classification metrics vs. epoch."""
    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Value")
    for m in list_of_metrics:
        x = hist[m]
        plt.plot(epochs[1:], x[1:], label=m)
    plt.legend()
    plt.show()