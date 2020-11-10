from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
# from celery import shared_task
# from celery_progress.backend import ProgressRecorder
from .forms import FileForm
from .metamotion_gather import Gather
from metamotion import MetaMotionDeviceNotFound, ConnectionError, LoggerError, Method

streaming_context = {"info_text": "After pressing this button, the connection with the sensor may take a bit long time", "form": FileForm()}
logging_context = {"info_text": "In this website, you can create loggers and download data for loggers previously created", "form": FileForm()}
sensor_gather = None

# Create your views here.

def index(request):
    return render(request, 'measure_controller/index.html')

def streaming(request):
    global streaming_context
    global sensor_gather
    if request.method == 'POST':
        sensor_gather.disconnect()
        sensor_gather.write_data_to_csv()
        return HttpResponseRedirect(reverse("streaming"))
    else:
        context = streaming_context
        streaming_context = {"info_text": "After pressing this button, the connection with the sensor may take a bit long time", "form": FileForm()}
        return render(request, 'measure_controller/streaming.html', context)

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
    global logging_context
    if request.method == 'POST':
        if 'file_name' in request.POST.keys():
            try:
                form = FileForm(request.POST)
                if form.is_valid():
                    sensor_gather = Gather(save_file=form.cleaned_data["file_name"], method=Method.LOGGING)
                    sensor_gather.get_data_from_loggers()
                    sensor_gather.disconnect()
                    sensor_gather.write_data_to_csv()
                    return HttpResponseRedirect(reverse("logging"))
            except (MetaMotionDeviceNotFound, ConnectionError):
                logging_context["info_text"] = "The connection with the sensor couldn't be made, try again"
            return HttpResponseRedirect(reverse("logging"))
        else:
            try:
                print("Conexión creando loggers")
                sensor_gather = Gather(method=Method.LOGGING)
                sensor_gather.init_loggers()
                sensor_gather.disconnect()
            except (MetaMotionDeviceNotFound, ConnectionError):
                logging_context["info_text"] = "The connection with the sensor couldn't be made, try again"
            except LoggerError:
                logging_context["info_text"] = "Failed to create loggers"
            return HttpResponseRedirect(reverse("logging"))

    elif request.method == 'GET':
        context = logging_context
        logging_context = {"info_text": "In this website, you can create loggers and download data for loggers previously created", "form": FileForm()}
        return render(request, 'measure_controller/logging.html', context)
