from django.shortcuts import render
from django.http.response import JsonResponse

from .models import *

# Create your views here.

def main(request):
    context = {
        "sensors": Sensor_ID.objects.all()
    }
    return render(request, 'Base/main.html', context)

def sensor(request, pk, lux, temperature, humidity):
    
    try:
        sensor_id = Sensor_ID.objects.get(sensor_id=pk)
    except Sensor_ID.DoesNotExist:
        return JsonResponse('Sensor ID does not exist')
    except ValueError:
        return JsonResponse('Invalid ID format')
    
    try: lux = float(lux)
    except ValueError: lux = None

    try: temperature = float(temperature)
    except ValueError: temperature = None

    try: humidity = float(humidity)
    except ValueError: humidity = None

    Sensor_Reading(
        sensor = sensor_id,
        temperature = temperature,
        humidity = humidity,
        lux = lux
    ).save()

    return JsonResponse('Success')