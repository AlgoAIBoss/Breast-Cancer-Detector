from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import BreastCancerChecker
from .forms import BreastCheckerForm
import joblib
import pandas as pd
import os


CURRENT_DIR = os.path.dirname(__file__)
model_file = os.path.join(
    CURRENT_DIR, 'model/gradient_breast_cancer_model.pkl')
svm = joblib.load(model_file)


# Create your views here.

def website(request):
    form = BreastCheckerForm()
    if request.method == 'POST':
        form = BreastCheckerForm(request.POST)
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        mean_radius = float(request.POST.get('mean_radius'))
        mean_perimeter = float(request.POST.get('mean_radius'))
        mean_texture = float(request.POST.get('mean_texture'))
        mean_area = float(request.POST.get('mean_area'))
        mean_smoothness = float(request.POST.get('mean_smoothness'))

        data = pd.DataFrame({
            'mean_radius': [mean_radius],
            'mean_texture': [mean_texture],
            'mean_perimeter': [mean_perimeter],
            'mean_area': [mean_area],
            'mean_smoothness': [mean_smoothness]
        })

        checker = svm.predict(data)
        if(checker == 1):
            messages.warning(request, 'Malignant')

        elif(checker == 0):
            messages.warning(request, 'Not cancerous')

        if form.is_valid():
            form.save()
        else:
            form = BreastCheckerForm()

    context = {'form': form}

    return render(request, 'home.html', context)
