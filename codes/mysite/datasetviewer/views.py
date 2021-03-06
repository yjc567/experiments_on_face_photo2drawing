import os

from django.http import HttpResponse
from django.shortcuts import render

from . import config
from .datas import get_dirs, get_image, get_overview, get_pose, get_missing_file
from .utils import dict_to_str

# Create your views here.
def return_an_error_page_if_DirNotFindError(func):
    def warpper(*args, **kw):
        try:
            return func(*args, **kw)
        except config.DirNotFindError as e:
            request = kw['request'] if 'request' in kw else args[0]
            return render(request, 'datasetviewer/error.html', {
                'error_message': e.args[0],
            })
    return warpper


def index(request):
    datasets = os.listdir(config.WC_datasets_dir)
    return render(request, 'datasetviewer/index.html', {'datasets': datasets})


@return_an_error_page_if_DirNotFindError
def overview(request, dataset_name, show_landmark=1):
    (images_dir, filenames_dir, landmarks_dir), messages = get_dirs(dataset_name)

    people_names, image_names, landmarks = get_overview(images_dir, filenames_dir, landmarks_dir)
    missing_file = get_missing_file(dataset_name)
    missing_file = dict_to_str(missing_file)

    return render(request, 'datasetviewer/overview.html', {
        'messages': messages,
        'dataset_name': dataset_name,
        'people_names_and_image_names': [(people_name, image_names[people_name]) for people_name in people_names],
        'show_landmark': show_landmark,
        'total_people': len(people_names),
        'total_images': sum(map(len, landmarks.values())),
        'missing_file': missing_file,
    })


@return_an_error_page_if_DirNotFindError
def detail(request, dataset_name, people_name, show_landmark=1):
    (images_dir, filenames_dir, landmarks_dir), messages = get_dirs(dataset_name)

    people_names, image_names, landmarks = get_overview(images_dir, filenames_dir, landmarks_dir)

    return render(request, 'datasetviewer/detail.html', {
        'messages': messages,
        'dataset_name': dataset_name,
        'people_name': people_name,
        'show_landmark': show_landmark,
        'image_names': image_names[people_name],
    })


@return_an_error_page_if_DirNotFindError
def view_image(request, dataset_name, people_name, image_name, show_landmark=1):
    image = get_image(dataset_name, people_name, image_name, show_landmark)

    return HttpResponse(image, content_type="image/jpg")


@return_an_error_page_if_DirNotFindError
def view_pose(request, dataset_name, people_name, image_name):
    # TODO: add expicit url to this view
    pose = get_pose(dataset_name, people_name, image_name)
    return HttpResponse(', '.join(map(str, map(int, pose))))


if __name__ == '__main__':
    overview(None, config.WC_original_dataset_name)