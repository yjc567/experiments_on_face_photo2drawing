import os

from django.http import HttpResponse
from django.shortcuts import render

try:
    from . import config
    from .utils import get_dirs, get_overview, get_image
except ImportError:
    import config
    from utils import get_dirs, get_overview, get_image

# Create your views here.
def index(request):
    datasets = os.listdir(config.WC_datasets_dir)
    return render(request, 'datasetviewer/index.html', {'datasets': datasets})


def overview(request, dataset_name, show_landmarks=1):
    try:
        (images_dir, filenames_dir, landmarks_dir), messages = get_dirs(dataset_name)
    except Exception as e:
        return render(request, 'datasetviewer/error.html', {
            'error_message': e.args[0],
        })

    people_names, image_names, landmarks = get_overview(images_dir, filenames_dir, landmarks_dir)
    # from IPython import embed; embed()

    return render(request, 'datasetviewer/overview.html', {
        'messages': messages,
        'dataset_name': dataset_name,
        'people_names': people_names,
        'show_landmarks': show_landmarks,
    })


def detail(request, dataset_name, people_name, show_landmarks=1):
    try:
        (images_dir, filenames_dir, landmarks_dir), messages = get_dirs(dataset_name)
    except Exception as e:
        return render(request, 'datasetviewer/error.html', {
            'error_message': e.args[0],
        })

    people_names, image_names, landmarks = get_overview(images_dir, filenames_dir, landmarks_dir)

    return render(request, 'datasetviewer/detail.html', {
        'messages': messages,
        'dataset_name': dataset_name,
        'people_name': people_name,
        'show_landmarks': show_landmarks,
        'image_names': image_names[people_name],
    })


def view_image(request, dataset_name, people_name, image_name, show_landmarks=1):
    try:
        (images_dir, filenames_dir, landmarks_dir), messages = get_dirs(dataset_name)
    except Exception as e:
        return render(request, 'datasetviewer/error.html', {
            'error_message': e.args[0],
        })

    image = get_image(images_dir, filenames_dir, landmarks_dir,\
                      people_name, image_name, show_landmarks)

    return HttpResponse(image, content_type="image/jpg")


if __name__ == '__main__':
    overview(None, config.WC_original_dataset_name)