import numpy as np


def baseline_data(event_stream, n_bins0=5, n_bins1=10):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            n_pixels = event.inst.num_pixels[telescope_id]
            r0_camera = event.r0.tel[telescope_id]

            adc_samples = r0_camera.adc_samples

            # Selection of only n_bins0 first samples and
            # n_bins1 last samples from given 50 samples
            adc_samples_first = adc_samples[:, 0:n_bins0-1]
            adc_samples_last = adc_samples[:, -n_bins1:]
            adc_samples = np.concatenate((adc_samples_first,
                                         adc_samples_last), axis=1)

            baseline = np.mean(adc_samples, axis=-1)
            std = np.std(adc_samples, axis=-1)

            r0_camera.baseline = baseline
            r0_camera.standard_deviation = std

        yield event


def baseline_simtel(event_stream):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            n_pixels = event.inst.num_pixels[telescope_id]
            r0_camera = event.r0.tel[telescope_id]
            r0_camera.baseline = (event.mc.tel[telescope_id].pedestal[0]
                                  / event.r0.tel[telescope_id].num_samples
                                  )
            # standard_deviation should be set up manualy and it should be
            # probably equal to value of 'fadc_noise' variable from simtel
            # configuration file
            r0_camera.standard_deviation = 1.5*np.ones(n_pixels)

        yield event


def save_mean_event_baseline(event_stream, filename):

    baseline = []
    std = []

    for i, event in enumerate(event_stream):

        for telescope_id in event.r0.tels_with_data:

            dl1_camera = event.dl1.tel[telescope_id]
            r0_camera = event.r0.tel[telescope_id]

            baseline.append(np.mean(
                r0_camera.baseline[dl1_camera.cleaning_mask]))
            std.append(np.mean(
                r0_camera.standard_deviation[dl1_camera.cleaning_mask]))

        yield event

    np.savetxt(filename, np.column_stack((baseline, std)), '%1.5f')
