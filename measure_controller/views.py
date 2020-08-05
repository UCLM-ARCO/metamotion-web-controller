from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .forms import FileForm
from .metamotion_gather import Gather
from metamotion import MetaMotionDeviceNotFound, ConnectionError

streaming_context = {"info_text": "After pressing this button, the connection with the sensor may take a bit long time", "form": FileForm()}
sensor_gather = None

# Create your views here.
def streaming(request):
    global streaming_context
    global sensor_gather
    if request.method == 'POST':
        sensor_gather.disconnect()
        sensor_gather.write_data_to_csv()
        return HttpResponseRedirect(reverse("streaming"))
    else:
        return render(request, 'measure_controller/streaming.html', streaming_context)

def gathering(request):
    global streaming_context
    global sensor_gather
    if request.method == 'POST':
        try:
            form = FileForm(request.POST)
            if form.is_valid():
                sensor_gather = Gather(save_file=form.cleaned_data["file_name"])
                sensor_gather.get_data_with_stream()
                return HttpResponseRedirect(reverse("gathering"))

        except (MetaMotionDeviceNotFound, ConnectionError):
            streaming_context["info_text"] = "The connection with the sensor couldn't be made, try again"
            return HttpResponseRedirect(reverse("streaming"))
    else:
        return render(request, 'measure_controller/gathering.html')

def logging(request):
    logging_context = {"form": FileForm()}
    if request.method == 'POST':
        if 'file_name' in request.POST.keys():
            try:
                print("Conexión con archivo")
                form = FileForm(request.POST)
                if form.is_valid():
                    print("Es valido")
                    sensor_gather = Gather(save_file=form.cleaned_data["file_name"])
                    sensor_gather.get_data_from_loggers()
                    sensor_gather.write_data_to_csv()
                    sensor_gather.disconnect()
                    return HttpResponseRedirect(reverse("logging"))
            except (MetaMotionDeviceNotFound, ConnectionError):
                print("Exception")
                streaming_context["info_text"] = "The connection with the sensor couldn't be made, try again"
            return HttpResponseRedirect(reverse("logging"))
        else:
            try:
                print("Conexión creando loggers")
                sensor_gather = Gather()
                sensor_gather.init_loggers()
                sensor_gather.disconnect()
            except (MetaMotionDeviceNotFound, ConnectionError):
                streaming_context["info_text"] = "The connection with the sensor couldn't be made, try again"
            return HttpResponseRedirect(reverse("logging"))

    elif request.method == 'GET':
        return render(request, 'measure_controller/logging.html', logging_context)
