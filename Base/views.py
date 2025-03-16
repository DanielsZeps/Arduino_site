from django.shortcuts import render
from django.http.response import JsonResponse

from .models import *

import datetime

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
        return JsonResponse({"response": "Sensor ID does not exist"})
    except ValueError:
        return JsonResponse({"response": "Invalid ID format"})
    
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
        lux = lux,
        time = datetime.datetime.now()
    ).save()

    return JsonResponse({"response": "Success"})

def sensor_data(request):
    response = {
        "data": []
    }
    for x in Sensor_ID.objects.all():
        try:
            data = x.readings.last()
            response["data"].append({
                "sensor": x.sensor_id,
                "lat": x.latitude,
                "lng": x.longitude,
                "lux": data.lux,
                "temp": data.temperature,
                "hum": data.humidity,
                "time": data.time,
            })
        except:
            pass
    return JsonResponse(response)