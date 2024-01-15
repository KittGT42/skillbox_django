from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'result': result,
        'a': a,
        'b': b,
    }
    return render(request, 'requestdataapp/request_query_params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {

    }
    return render(request, 'requestdataapp/user_bio_form.html', context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        my_file = request.FILES['myfile']
        fs = FileSystemStorage()
        file_name = fs.save(my_file.name, my_file)
        print('saved file', file_name)

    context = {}
    return render(request, 'requestdataapp/file_upload.html', context=context)