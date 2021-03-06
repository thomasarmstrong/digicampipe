'''
Something with baseline stability

Usage:
  baseline_stability <fitsfile>

Options:
  -h --help     Show this screen.
'''
from digicampipe.io.event_stream import event_stream
import matplotlib.pyplot as plt
import numpy as np
from docopt import docopt
from tqdm import tqdm


def main(infile):

    baselines = []
    for data in tqdm(event_stream(infile)):
        for r0 in data.r0.tel.values():
            baselines.append(r0.digicam_baseline)
    baselines = np.array(baselines)

    plt.figure()
    plt.plot(baselines[0])
    plt.plot(baselines[1])
    plt.plot(baselines[2])
    plt.plot(baselines[-1])
    plt.show()

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
