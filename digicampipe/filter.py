import numpy as np
from event_stream import event_stream
from digicampipe.skimmer import skim_events, compute_discrimination_variable, compute_patch_coordinates


def filter_events(event_stream):

    patch_coordinates = compute_patch_coordinates()

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            r0_container = event.r0.tel[telescope_id]

            variable = compute_discrimination_variable(r0_container=r0_container, patch_coordinates=patch_coordinates)

            trigger_time, total_time_above_threshold, max_time_above_threshold, n_patches_above_threshold, sigma, nimp = variable

            if not nimp:

                print(n_patches_above_threshold)

                if n_patches_above_threshold > 5:

                    yield event



if __name__ == '__main__':

    from digicampipe.skimmer import skim_events
    from digicamviewer.viewer import EventViewer

    camera_config_file = '/home/alispach/Documents/PhD/ctasoft/CTS/config/camera_config.cfg'

    directory = '/home/alispach/blackmonkey/'
    filename = directory + 'CameraDigicam@sst1mserver_0_000.%d.fits.fz'
    file_list = [filename % number for number in range(30, 165)]
    data_stream = event_stream(file_list=file_list, expert_mode=True)
    data_stream = filter_events(data_stream)
    #  filtered_data = filter_events(event_stream)

#    data = skim_events(data_stream)
#    np.savez('temp.npz', **data)

    display = EventViewer(data_stream, camera_config_file=camera_config_file, scale='lin')
    display.draw()
    0/0
    data = np.load('temp.npz')

    print(data['time_trigger'])

    import matplotlib
    import matplotlib.pyplot as plt

    plt.figure()
    plt.hist(data['time_trigger'], log=True)

    plt.figure()
    plt.hist(data['time_total'], log=True)

    plt.figure()
    plt.hist(data['time_max'], log=True)

    plt.figure()
    plt.hist(data['n_patches'], log=True)

    plt.figure()
    # plt.hist(data['shower_spread'], log=True)

    from scipy.stats import expon

    param = expon.fit(np.diff(data['time_trigger']), floc=0)
    plt.figure()
    hist = plt.hist(np.diff(data['time_trigger']), log=True)
    n_entries = np.sum(hist[0])
    bin_width = hist[1][1] - hist[1][0]
    pdf_fit = expon(loc=param[0], scale=param[1])
    plt.plot(hist[1], n_entries * bin_width * pdf_fit.pdf(hist[1]),
             label='$f_{trigger}$ = %0.2f [Hz]' % (1E9 / param[1]))
    plt.legend(loc='best')

    for key_1, val_1 in data.items():
        for key_2, val_2 in data.items():

            if key_1 in ['time_trigger', 'shower_spread'] or key_2 in ['time_trigger', 'shower_spread']:
              continue

            num = 10
            bins = [np.linspace(np.min(val_1), np.max(val_1), num=num), np.linspace(np.min(val_2), np.max(val_2), num=num)]
            plt.figure()
            plt.hist2d(val_1, val_2, bins=bins, norm=matplotlib.colors.LogNorm())
            plt.xlabel(key_1)
            plt.ylabel(key_2)

    plt.show()
