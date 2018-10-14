import hashlib
import os
import shutil

import cv2
import numpy as np

from . import config


def dataset_iterator(dataset_name):
    '''
    return (people_name, image_type, image_name, landmark) of each image
    '''
    from .datas import get_dirs, get_overview

    (images_dir, filenames_dir, landmarks_dir), messages = get_dirs(dataset_name)
    people_names, image_names, landmarks = get_overview(images_dir, filenames_dir, landmarks_dir)

    for people_name in people_names:
        for image_type in ('c', 'p',):
            for image_name in image_names[people_name][image_type]:
                yield people_name, image_type, image_name, landmarks[people_name][image_name]


def perpare_dataset_dir(new_dataset_name, file):
        # makedir and backup
        version = sum(map(lambda x: x.startswith(new_dataset_name), os.listdir(config.WC_datasets_dir)))
        new_dataset_dir = os.path.join(config.WC_datasets_dir, '%s_v%03d' % (new_dataset_name, version))
        os.makedirs(new_dataset_dir)
        shutil.copy(file, new_dataset_dir)

        # md5 check
        m = hashlib.md5()
        with open(file, 'rb') as f:
            m.update(f.read())
        md5_path = os.path.join(new_dataset_dir, 'md5')
        if not os.path.exists(md5_path):
            with open(md5_path, 'wb') as md5_file:
                md5_file.write(m.digest())
        else:
            with open(md5_path, 'rb') as md5_file:
                assert md5_file.read() == m.digest(), 'You can not change file: %s to override existing dataset!' % file
        
        return new_dataset_dir


def im_str_to_np(im_str):
    im = np.fromstring(im_str, np.uint8)
    im = cv2.imdecode(im, cv2.IMREAD_COLOR)
    return im
