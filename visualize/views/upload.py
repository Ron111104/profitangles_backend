from django.shortcuts import render

def upload_file(request):
    return render(request, 'visualize/upload.html')
