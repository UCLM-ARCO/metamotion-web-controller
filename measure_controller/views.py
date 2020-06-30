from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .forms import FileForm
from .metamotion_gather import Gather
from metamotion import MetaMotionDeviceNotFound, ConnectionError
from time import sleep

context = {"info_text": "After pressing this button, the connection with the sensor may take a bit long time", "form": FileForm()}
sensor_gather = None

# Create your views here.
def index(request):
    global context
    global sensor_gather
    if request.method == 'POST':
        sensor_gather.write_data_to_csv()
        sensor_gather.disconnect()
        sleep(3) #added sleep to ensure disconnection
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'measure_controller/index.html', context)

def gathering(request):
    global context
    global sensor_gather
    if request.method == 'POST':
        try:
            form = FileForm(request.POST)
            if form.is_valid():
                sensor_gather = Gather(save_file=form.cleaned_data["file_name"])
                sensor_gather.get_data_with_stream()
                return HttpResponseRedirect(reverse("gathering"))

        except (MetaMotionDeviceNotFound, ConnectionError):
            context["info_text"] = "The connection with the sensor couldn't be made, try again"
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'measure_controller/gathering.html')