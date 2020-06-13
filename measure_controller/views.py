from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .metamotion_gather import Gather
from django.urls import reverse
from django.template import loader

is_measuring = False
context = {"button_text": "Begin Measure"}
sensor_gather = None

# Create your views here.
def index(request):
    global is_measuring
    global context 
    global sensor_gather
    if request.method == 'POST':
        is_measuring = not is_measuring

        if is_measuring:
            context = {"button_text": "Stop Measure"}
            sensor_gather = Gather()
            sensor_gather.get_data_with_stream()
        else:
            context = {"button_text": "Begin Measure"}
            sensor_gather.write_data_to_csv()
            sensor_gather.disconnect()
        
        return HttpResponseRedirect(reverse("index"))
        # return render(request, 'measure_controller/index.html', context)

    else:
        # context = {"button_text": "Begin Measure"}
        return render(request, 'measure_controller/index.html', context)

