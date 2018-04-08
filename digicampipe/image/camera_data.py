from pkg_resources import resource_filename
from decimal import Decimal, ROUND_HALF_EVEN
import numpy as np
import os
import time

from matplotlib import pyplot as plt
from cts_core.camera import Camera
from astropy.io import fits
from astropy import units as u
from ctapipe.image.hillas import hillas_parameters
from scipy.interpolate import LinearNDInterpolator

from digicampipe.io.event_stream import event_stream
from digicampipe.calib.camera import filter, r0, r1, dl0, dl1, dl2, random_triggers
from digicampipe.utils import geometry
from digicampipe.utils import utils
from digicampipe.image.cones_image import get_pixel_nvs
import simtel_baseline

__all__ = [
    "CameraData",
    "animate",
]

datafile_default = resource_filename(
    'digicampipe',
    os.path.join(
        'tests',
        'resources',
        'SST1M01_0_000.072.fits.fz'
    )
)
digicam_config_file_default = resource_filename(
    'digicampipe',
    os.path.join(
        'tests',
        'resources',
        'camera_config.cfg'
    )
)


def animate(data, n_event_max=np.inf):
    plt.ion()
    first = True
    plt.figure()
    for i, data_event in enumerate(data):
        n_sample = data_event.shape[2]
        for t in range(n_sample):
            title_text = 'event: %i / %i\nt: %i / %i ns' % \
                         (i + 1, len(data), (t + 1) * 4, n_sample * 4)
            if first:
                img = plt.imshow(data_event[:, :, t],
                                 vmin=-500, vmax=500, cmap='seismic')
                first = False
                plt.colorbar()
                title = plt.title(title_text)
            else:
                img.set_array(data_event[:, :, t])
                title.set_text(title_text)
            plt.pause(.04)
            #if t == 10:
            #    plt.pause(2)
        if i >= n_event_max - 1:
            break
    plt.ioff()


class CameraData(object):
    _fits = None

    def __init__(
            self,
            filename,
            datafiles_list=None,
            digicam_config_file=digicam_config_file_default,
            unwanted_pixels=None,
            flags=None,
            min_adc=None,
            print_every=100,
            max_events=None,
            mc=False
    ):
        self.digicam_config_file = digicam_config_file
        self.digicam = Camera(_config_file=self.digicam_config_file)
        self.geo = geometry.generate_geometry_from_camera(camera=self.digicam)
        if unwanted_pixels is not None:
            self.unwanted_pixels = unwanted_pixels
        else:
            self.unwanted_pixels = []
        self.flags = flags
        self.min_adc = min_adc
        self.max_events = max_events
        self.mc = mc
        if datafiles_list is not None:
            self.create_fits_file(filename, datafiles_list,
                                  print_every=print_every)
        self._fits = fits.open(filename, memmap=True)
        self.n_event = len(self._fits)
        # print('shape of data from file', self._fits[0].data.shape)
        self.event_shape = self._fits[0].data.shape
        self.data_shuffle_indexes = np.random.RandomState(seed=42).permutation(
            self.n_event
        )

    def __del__(self):
        if self._fits is not None:
            self._fits.close()

    def _new_event_stream(self, datafiles_list):
        time_integration_options = {'mask': None,
                                    'mask_edges': None,
                                    'peak': None,
                                    'window_start': 3,
                                    'window_width': 15,
                                    'threshold_saturation': np.inf,
                                    'n_samples': 50,
                                    'timing_width': 10,
                                    'central_sample': 11}
        peak_position = utils.fake_timing_hist(
            time_integration_options['n_samples'],
            time_integration_options['timing_width'],
            time_integration_options['central_sample'])

        (
            time_integration_options['peak'],
            time_integration_options['mask'],
            time_integration_options['mask_edges']
        ) = utils.generate_timing_mask(
            time_integration_options['window_start'],
            time_integration_options['window_width'],
            peak_position
        )
        additional_mask = np.ones(1296, dtype=bool)
        if self.unwanted_pixels:
            additional_mask[self.unwanted_pixels] = 0
            additional_mask = additional_mask > 0
        picture_threshold = 15
        boundary_threshold = 10
        shower_distance = 200 * u.mm
        events_stream = event_stream(
            file_list=datafiles_list,
            camera_geometry=self.geo,
            camera=self.digicam,
            expert_mode=True,
            max_events=self.max_events,
            mc=self.mc
        )
        if self.unwanted_pixels is not None:
            events_stream = filter.set_pixels_to_zero(
                events_stream,
                unwanted_pixels=self.unwanted_pixels
            )
        if self.mc:
            events_stream = simtel_baseline.fill_baseline_r0(
                events_stream, n_bins0=9, n_bins1=30, method='data'
            )
        else:
            events_stream = random_triggers.fill_baseline_r0(events_stream, n_bins=100)
            # Stop events that are not triggered by DigiCam algorithm
            # (end of clocked triggered events)
            if self.flags is not None:
                events_stream = filter.filter_event_types(
                    events_stream,
                    flags=self.flags
                )
            events_stream = filter.filter_missing_baseline(events_stream)
        events_stream = r1.calibrate_to_r1(events_stream, None)
        # Run the dl0 calibration (data reduction, does nothing)
        events_stream = dl0.calibrate_to_dl0(events_stream)
        # Run the dl1 calibration (compute charge in photons + cleaning)
        events_stream = dl1.calibrate_to_dl1(events_stream,
                                           time_integration_options,
                                           additional_mask=additional_mask,
                                           picture_threshold=picture_threshold,
                                           boundary_threshold=boundary_threshold)
        """
        # Return only showers with total number of p.e. above min_photon
        events_stream = filter.filter_shower(
            events_stream, min_photon=args['--min_photon'])
        """
        # Run the dl2 calibration (Hillas)
        events_stream = dl2.calibrate_to_dl2(
            events_stream, reclean=True, shower_distance=shower_distance)
        wanted_pixels = np.arange(len(self.digicam.Pixels))
        if self.unwanted_pixels is not None:
            mask = np.ones_like(wanted_pixels, dtype=bool)
            mask[self.unwanted_pixels] = False
            wanted_pixels = wanted_pixels[mask]
        for event in events_stream:
            tel = event.r0.tels_with_data[0]
            r0_cont = event.r0.tel[tel]
            adc_samples = r0_cont.adc_samples[wanted_pixels, :]
            if isinstance(r0_cont.digicam_baseline, np.ndarray):
                baseline = np.reshape(r0_cont.digicam_baseline[wanted_pixels],
                                      (-1, 1))
            else:
                if isinstance(r0_cont.baseline, np.ndarray):
                    baseline = np.reshape(r0_cont.baseline[wanted_pixels],
                                      (-1, 1))
                    r0_cont.digicam_baseline = np.round(baseline)
                else:
                    print('WARNING: no baseline available !')
            if self.min_adc is None:
                yield event
            elif np.any(adc_samples - baseline > self.min_adc):
                yield event

    def create_fits_file(self, filename, datafiles_list,
                         print_every=500):
        nvs = CameraData.get_pixels_pos_in_skew_base(
            self.digicam_config_file
        )
        n_pixel_u, n_pixel_v = (np.max(nvs, axis=0) + 1).tolist()
        pix_pos = np.array([self.geo.pix_x, self.geo.pix_y]).transpose()
        image_x, image_y = (np.linspace(-504, 504, 48).reshape(-1,1), np.linspace(-504, 504, 48))
        n_event, n_sample = self.get_data_size(datafiles_list)
        if os.path.isfile(filename):
            os.remove(filename)
        events_stream = self._new_event_stream(datafiles_list)
        n_unwanted_pixel = 0
        if self.unwanted_pixels is not None:
            n_unwanted_pixel = len(self.unwanted_pixels)
            wanted_pixels = []
            for i in range(pix_pos.shape[0]):
                if i not in self.unwanted_pixels:
                    wanted_pixels.append(i)
        else:
            wanted_pixels = range(len(nvs))
        hdr = fits.Header()
        hdr['SIMPLE'] = (True, 'conforms to FITS standard')
        hdr['BITPIX'] = (16, 'array data type')  # dtype=int16
        hdr['NAXIS'] = (3, 'number of array dimensions')
        hdr['NAXIS1'] = (n_sample, 'number of samples per event')
        hdr['NAXIS2'] = (n_pixel_u, 'number of horizontal pixels in image')
        hdr['NAXIS3'] = (n_pixel_v, 'number of vertical pixels in image')
        hdr['EXTEND'] = True
        event_loaded = 0
        for event in events_stream:
            tel = event.r0.tels_with_data[0]
            r0 = event.r0.tel[tel]
            adc_samples = np.array(r0.adc_samples)
            hillas = event.dl2.shower
            psi = hillas.psi.rad
            rot_angle = psi + np.pi/2
            cen_x = u.Quantity(hillas.cen_x).value
            cen_y = u.Quantity(hillas.cen_y).value
            hdr['rotation'] = (rot_angle, 'rotation applied in rad')
            hdr['offset_x'] = (-cen_x, 'horizontal offset applied')
            hdr['offset_y'] = (-cen_y, 'vertical offset applied')
            baseline = r0.digicam_baseline
            if self.mc:
                hdr['energy'] = u.Quantity(event.mc.energy).value
                hdr['alt'] = u.Quantity(event.mc.alt).value
                hdr['az'] = u.Quantity(event.mc.az).value
                hdr['core_x'] = u.Quantity(event.mc.core_x).value
                hdr['core_y'] = u.Quantity(event.mc.core_y).value
                hdr['HFstInt'] = (u.Quantity(event.mc.h_first_int).value,
                                  'Height of first interaction.')
            data_event = np.zeros([n_pixel_u, n_pixel_v, n_sample],
                                  dtype=np.int16)
            pix_pos_translate = pix_pos - np.array([cen_x, cen_y])
            pix_pos_transform = pix_pos_translate.dot(
                np.array([[np.cos(rot_angle), np.sin(-rot_angle)], [np.sin(rot_angle), np.cos(rot_angle)]])
            )
            for t in range(n_sample):
                f_2d_interp = LinearNDInterpolator(
                    np.vstack((pix_pos_transform[wanted_pixels], pix_pos_transform[self.unwanted_pixels])),
                    np.hstack((adc_samples[wanted_pixels, t] - baseline[wanted_pixels].reshape(-1),
                               np.zeros((n_unwanted_pixel,)))),
                    fill_value=0)
                data_event[:, :, t] = f_2d_interp(image_x, image_y)
            event_loaded += 1
            fits.append(filename, data_event, hdr)
            if event_loaded % print_every == 0:
                print(event_loaded, "events loaded")
        print('closing stream after', event_loaded, "events loaded")
        events_stream.close()

    def get_data_size(self, datafiles_list):
        print("getting size of the event stream ...")
        events_stream = self._new_event_stream(datafiles_list)
        event = next(events_stream)
        tel = event.r0.tels_with_data[0]
        r0 = event.r0.tel[tel]
        adc_samples = r0.adc_samples
        n_pixels, n_samples = adc_samples.shape
        size = 1
        for _ in events_stream:
            size += 1
        events_stream.close()
        print("got", size, 'events with', n_samples, 'samples')
        return size, n_samples

    @staticmethod
    def get_pixels_pos_in_skew_base(camera_config_file):
        pixel_nvs = get_pixel_nvs(digicam_config_file=camera_config_file)
        pixel_nvs = np.array(pixel_nvs)
        nvs_from_orig = pixel_nvs - np.min(pixel_nvs, axis=1, keepdims=True)
        precision = Decimal('0.1')
        nvs_dec = np.array([
            [
                Decimal(n1*3).quantize(precision, rounding=ROUND_HALF_EVEN)/3,
                Decimal(n2*3).quantize(precision, rounding=ROUND_HALF_EVEN)/3,
            ]
            for n1, n2 in nvs_from_orig.transpose()
        ])
        nvs = nvs_dec.astype(int)
        return nvs

    def get_used_pixel_in_skew_base(self):
        nvs = self.get_pixels_pos_in_skew_base(self.digicam_config_file)
        nvs[self.unwanted_pixels]
        mask_shape =  np.max(nvs, axis=0)
        mask = np.zeros(mask_shape+1)
        for i, (x, y) in enumerate(nvs):
            if self.unwanted_pixels is not None and i in self.unwanted_pixels:
                continue
            mask[x, y] = 1
        return mask

    def get_batch(self, batch_size=None, n_sample=None, type_set='train'):
        #get indexes for the 3 types of sets
        n_event = self.n_event
        n_train = int(0.8 * n_event)
        n_val = int(0.1 * n_event)
        n_test = n_event - n_train - n_val
        train_indexes, val_indexes, test_indexes = np.split(
            self.data_shuffle_indexes,
            [n_train, n_train+n_val],
            axis=0
        )
        if type_set == 'train':
            if batch_size is None:
                indexes = train_indexes[np.random.permutation(n_train)]
            else:
                indexes = train_indexes[
                    np.random.permutation(n_train)[:batch_size]
                ]
        elif type_set == 'val':
            if batch_size is None:
                indexes = val_indexes[np.random.permutation(n_val)]
            else:
                indexes = val_indexes[
                    np.random.permutation(n_val)[:batch_size]
                ]
        elif type_set == 'test':
            print('WARNING: test data should only be used once !')
            if batch_size is None:
                indexes = test_indexes[np.random.permutation(n_test)]
            else:
                indexes = test_indexes[
                    np.random.permutation(n_test)[:batch_size]
                ]
        else:
            print('ERROR: unknown type_set:', type_set)
            return

        if n_sample is None:
            n_sample = self.event_shape[-1]
        events = {}
        events['data'] = np.zeros((batch_size, self.event_shape[0],
                                   self.event_shape[1], n_sample))
        events['rotation'] = np.zeros((batch_size, ))
        events['offset_x'] = np.zeros((batch_size, ))
        events['offset_y'] = np.zeros((batch_size, ))
        if self.mc:
            events['energy'] = np.zeros((batch_size, ))
            events['alt'] = np.zeros((batch_size, ))
            events['az'] = np.zeros((batch_size, ))
            events['core_x'] = np.zeros((batch_size, ))
            events['core_y'] = np.zeros((batch_size, ))
            events['HFstInt'] = np.zeros((batch_size, ))
        for i, index in enumerate(indexes):
            event = self._fits[index]
            events['data'][i, :, :, :] = \
                event.data[:, :, :n_sample]
            events['rotation'][i] = event.header['rotation']
            events['offset_x'][i] = event.header['offset_x']
            events['offset_y'][i] = event.header['offset_y']
            if self.mc:
                events['energy'][i] = event.header['energy']
                events['alt'][i] = event.header['alt']
                events['az'][i] = event.header['az']
                events['core_x'][i] = event.header['core_x']
                events['core_y'][i] = event.header['core_y']
                events['HFstInt'][i] = event.header['HFstInt']
        return events

    def animate(self, batch_size=None, type_set='train'):
        events = self.get_batch(batch_size, type_set=type_set)
        animate(events['data'])


def create_file(camera_data, datafiles_list=None, print_every=100):
    # create fits file
    datafile_crab = [
        '/sst1m/raw/2017/10/30/SST1M01/SST1M01_20171030.%03d.fits.fz'
        % i for i in range(11,92)
    ]
    pixel_not_wanted = [
        1038, 1039, 1002, 1003, 1004, 966, 967, 968, 930, 931, 932, 896,
        1085, 1117, 1118, 1119, 1120, 1146, 1147, 1148, 1149, 1150, 1151,
        1152, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181,
        1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206,
        1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1239, 1240, 1241,
        1242, 1243, 1256, 1257
    ]
    if datafiles_list is None:
        datafiles_list = datafile_crab
    CameraData(
        camera_data, datafiles_list=datafiles_list,
        digicam_config_file=digicam_config_file_default,
        unwanted_pixels=pixel_not_wanted,
        flags=[1],
        min_adc=100,
        print_every=print_every
    )


def show_file(camera_data, batch_size=None, type_set='train'):
    # load fits file:
    data = CameraData(camera_data)
    # show data:
    data.animate(batch_size=batch_size, type_set=type_set)


if __name__ == '__main__':
    # MC files from
    # http://pc048b.fzu.cz/sst-simulations/cta-prod3-sst-dc/
    mc_dir = '/home/yves/ctasoft/digicampipe/data/mc_simtel'
    all_file_list = os.listdir(mc_dir)
    mc_proton_files = []
    mc_gamma_files = []
    for file in all_file_list:
        if file.endswith('.simtel.gz'):
            if file.startswith('proton'):
                mc_proton_files.append(os.path.join(mc_dir, file))
            if file.startswith('gamma'):
                mc_gamma_files.append(os.path.join(mc_dir, file))
    #create_file(camera_data,
    #            print_every=10)
    proton_data = os.path.join('/home/yves/ctasoft/digicampipe/data',
                               'proton_data_mc.fits')
    CameraData(proton_data, datafiles_list=mc_proton_files,
               digicam_config_file=digicam_config_file_default,
               min_adc=10,
               print_every=100,
               max_events=None,
               mc=True)
    show_file(proton_data, batch_size=10)

    """
    gamma_data = os.path.join('/home/yves/ctasoft/digicampipe/data',
                              'gamma_data_mc.fits')
    CameraData(gamma_data, datafiles_list=mc_gamma_files,
               digicam_config_file=digicam_config_file_default,
               min_adc=10,
               print_every=100,
               max_events=10000,
               mc=True)
    show_file(gamma_data)
    """