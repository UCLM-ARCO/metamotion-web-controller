from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .forms import FileForm
from .metamotion_gather import Gather
from metamotion import MetaMotionDeviceNotFound, ConnectionError

context = {"info_text": "After pressing this button, the connection with the sensor may take a bit long time", "form": FileForm()}
sensor_gather = None

# Create your views here.
def index(request):
    # global is_measuring
    # global context 
    # global sensor_gather
    # if request.method == 'POST':
    #     is_measuring = not is_measuring

    #     if is_measuring:
    #         context = {
    #             "button_text": "Stop Measure",
    #             "info_text": "The sensor is measuring, press the button when the exercise finalized"}
    #         try:
    #             sensor_gather = Gather()
    #             sensor_gather.get_data_with_stream()
    #         except (MetaMotionDeviceNotFound, ConnectionError):
    #             context["button_text"] = "Begin Measure"
    #             context["info_text"] = "The connection with the sensor couldn't be made, try again"
    #             is_measuring = False
    #     else:
    #         context = {
    #             "button_text": "Begin Measure",
    #             "info_text": "After pressing this button, the connection with the sensor may take a bit long time"}
    #         sensor_gather.write_data_to_csv()
    #         sensor_gather.disconnect()
        
    #     return HttpResponseRedirect(reverse("index"))

    # else:
    #     return render(request, 'measure_controller/index.html', context)
    global context
    global sensor_gather
    if request.method == 'POST':
        sensor_gather.write_data_to_csv()
        sensor_gather.disconnect()
        # return render(request, 'measure_controller/index.html', context)
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
                print("In if")
                print(form["file_name"].value())
                sensor_gather = Gather(save_file=form.cleaned_data["file_name"])
                sensor_gather.get_data_with_stream()
            # return render(request, 'measure_controller/gathering.html')
                return HttpResponseRedirect(reverse("gathering"))

        except (MetaMotionDeviceNotFound, ConnectionError):
            context["info_text"] = "The connection with the sensor couldn't be made, try again"
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'measure_controller/gathering.html')



        
