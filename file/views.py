from django.shortcuts import render
from .models import File
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@login_required(login_url= 'login')
def uploadFile(request):
    if request.method=='POST':
        try:
            file = request.FILES.get('file')
            if file:
                File.objects.create(doc=file, user=request.user)
                messages.success(request,'Your file has been uploaded successfully!')
                return render(request, 'opsUserDashboard.html')
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            messages.error(request, 'An error occurred while uploading the file')
            return render(request, 'opsUserDashboard.html')
        
    return render(request, 'opsUserDashboard.html')

@login_required(login_url= 'login')
def downloadFile(request):
    files= File.objects.all()
    return render(request, 'clientUserDashboard.html', {'files':files})