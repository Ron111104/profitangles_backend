from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os

def upload_file(request):
    try:
        if request.method == "POST":
            # Handle file upload
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                return HttpResponse("No file uploaded.", status=400)

            # Save the uploaded file
            fs = FileSystemStorage(location=os.path.join("media", "uploads"))
            os.makedirs(fs.location, exist_ok=True)  # Ensure directory exists
            filename = fs.save(csv_file.name, csv_file)

            # Pass context to display buttons
            return render(request, "visualize/upload.html", {"csv_file_uploaded": True})
        
        # Render the upload form for GET request
        return render(request, "visualize/upload.html", {"csv_file_uploaded": False})

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
