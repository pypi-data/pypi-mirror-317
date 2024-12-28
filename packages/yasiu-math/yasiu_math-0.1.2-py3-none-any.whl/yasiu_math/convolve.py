import numpy as _np

from scipy.signal import convolve as _convolve


def moving_average(array, radius=1, padding="try", kernel_type="avg", kernel_exp=2):
    """
    Rolling average function with edge treatment.

    :param array: list or 1d np.ndarray

    :param smoothing_radius:
    radius
     radius of kernel, `kernel size = 2 * radius + 1`

    :param padding: str
    :type padding: str

    padding: str
        try - calculates number using every value it has without padding

        full - extends results to padded numbers

        same - calculates average for every number, uses 0 vals

        valid- returns only average number that have full frame of values

        keep - keep raw values that can not be calculated

    :param kernel_type:
    kernel_type: str
        avg - all values have equal weight (blurred image)

        linear - linear weights, same as exp type, with `exponent weight = 1`
            example weights before norm:
            [1, 2, 3, 2, 1]

        exp - raising weight to given power in `kernel_exp` variable
            example weights before norm with kernel_exp = 2:
            [1, 4, 9, 4, 1]

    :param kernel_exp:
    kernel_exp : float, must be in range <0, inf>
     Non linearity exponent, before normalization
     only for `kernel_type='exp'`
     kernel_value ^ exponent

    :return:

    """
    smoothing_frames = 1 + 2 * abs(radius)
    if smoothing_frames > len(array):
        return array

    if kernel_type == "avg":
        kernel = _np.ones(smoothing_frames) / smoothing_frames

    elif kernel_type == "linear":
        kernel = _np.arange(radius + 1) + 1
        kernel = _np.concatenate([kernel[:-1], _np.flip(kernel)])
        kernel = kernel / kernel.sum()

    elif kernel_type == 'exp':
        "Exponential"
        kernel = _np.arange(radius + 1) + 1
        kernel = _np.concatenate([kernel[:-1], _np.flip(kernel)])
        kernel = kernel ** kernel_exp
        kernel = kernel / kernel.sum()
    else:
        raise KeyError(
            f"Invalid kernel_type{kernel_type}. Use one: exp,linear,avg.")

    if padding == "same":
        out = _convolve(array, kernel, 'same')

    elif padding == "try" or padding == 'keep':
        out = _convolve(array, kernel, 'valid')

        if padding == "try":
            left, right = convolve_array_edges(array, radius)
            # a, b, c = len(left), len(out), len(right)
            # print(radius,a + b + c, a, b, c)
            # print(f"\tKernel: {kernel.shape}")

        else:
            left = array[:radius]
            right = array[-radius:]
            # print(len(left), len(out), len(right))

        out = _np.concatenate([left, out, right])

    elif padding == "full":
        out = _convolve(array, kernel, 'full')

    elif padding == 'valid':
        "valid"
        out = _convolve(array, kernel, 'valid')
    else:
        raise KeyError(
            f"Invalid padding key:{padding}. Use one: valid,same,try,keep.")

    # posx[:smoothing_frames] = tempx[:smoothing_frames]
    return out


def convolve_array_edges(arr, radius):
    """
    Convolve array edges. Using available numbers.
    Sub function.

    Args:
        arr:
        radius:

    Returns
     left - convoluted list of left side

     right - convoluted list of right side

    """
    # size = 1 + 2 * abs(radius)

    left = _np.zeros(radius)
    right = _np.zeros(radius)

    if radius > 0:
        csum = 0
        for i, num in enumerate(arr[:radius * 2]):
            csum += num
            if i >= radius:
                left[i - radius] = csum / (i + 1)

        csum = 0
        for i, num in enumerate(arr[:-radius * 2 - 1:-1]):
            csum += num
            if i >= radius:
                right[i - radius] = csum / (i + 1)

    return left, right


__all__ = [
    "moving_average",
]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.style import use
    import os

    use("ggplot")

    arr = _np.arange(40).reshape(-1, 2).T/20
    arr = arr.ravel()
    noise = _np.sin(arr*8)/10
    arr += noise
    radius = 5

    plt.figure(figsize=(7, 5), dpi=150)
    plt.subplot(2, 1, 1)
    plt.title("Edge handling comparison")
    plt.plot(arr, label="True value", linewidth=3, alpha=0.5)

    smooth1 = moving_average(arr, radius=radius)
    plt.plot(smooth1, label="Smoothing: default")

    smooth1 = moving_average(arr, radius=radius, padding='keep')
    plt.plot(smooth1, label="Smoothing: keep")

    smooth1 = moving_average(arr, radius=radius, padding='same')
    plt.plot(smooth1, label="Smoothing: same (padding 0)")

    plt.legend(loc='lower right', prop={'size': 6})
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    plt.title("Sample weight comparison")
    plt.plot(arr, label="True value", linewidth=3, alpha=0.5)

    smooth1 = moving_average(arr, radius=radius)
    plt.plot(smooth1, label="Smoothing weights: equal")

    smooth1 = moving_average(arr, radius=radius, kernel_type='linear')
    plt.plot(smooth1, label="Smoothing weights: linear")

    smooth1 = moving_average(arr, radius=radius, kernel_type='exp')
    plt.plot(smooth1, label="Smoothing weights: exponential (2)")

    smooth1 = moving_average(
        arr, radius=radius, kernel_type='exp', kernel_exp=4)
    plt.plot(smooth1, label="Smoothing weights: exponential (4)")

    plt.suptitle(f"Smoothing signal with window size: {2*radius+1}")
    plt.legend(loc='lower right', prop={'size': 6})
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(
        __file__), "..", "pics", "convolveComparison.png"))
    # plt.show()
