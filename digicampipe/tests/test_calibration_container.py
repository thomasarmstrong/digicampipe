from digicampipe.io.event_stream import calibration_event_stream, event_stream


def test_calibration_event_stream():

    path = 'test'
    max_events = 10
    telescope_id = 1

    calib_stream = calibration_event_stream(path, telescope_id, max_events)
    obs_stream = event_stream(path, max_events=max_events)

    for event_calib, event_obs in zip(calib_stream, obs_stream):

        assert event_calib.data.adc_samples == \
               event_obs.r0.tel[telescope_id].adc_samples
        assert event_calib.data.digicam_baseline == \
               event_obs.r0.tel[telescope_id].digicam_baseline

        assert event_calib.n_pixels == \
               event_obs.r0.tel[telescope_id].adc_samples.shape[0]
