from django.http import JsonResponse
from .models import Parking
from django.utils import timezone
from django.shortcuts import render
from django.db import models
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def home(request):
    try:
        parking = Parking.objects.first()
        total_spaces = parking.total_spaces if parking else 0
        available_spaces = parking.available_spaces if parking else 0
        context = {
            'total_spaces': total_spaces,
            'available_spaces': available_spaces,
            'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return render(request, 'parking.html', context)
    except Exception as e:
        logger.error(f"Error fetching parking info: {e}", exc_info=True)
        return render(request, 'parking.html', {'error': 'Internal Server Error'})

def parking_info(request):
    try:
        total_spaces = Parking.objects.aggregate(total=models.Sum('total_spaces'))['total'] or 0
        available_spaces = Parking.objects.aggregate(available=models.Sum('available_spaces'))['available'] or 0
        data = {
            'total_spaces': total_spaces,
            'available_spaces': available_spaces,
            'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')  # Formatear la fecha en el servidor
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error fetching parking info: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

@csrf_exempt
def car_enter(request):
    try:
        parking = Parking.objects.first()
        if parking.available_spaces > 0:
            parking.available_spaces -= 1
            parking.save()
        data = {
            'available_spaces': parking.available_spaces,
            'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')  # Formatear la fecha en el servidor
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error updating parking info: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

@csrf_exempt
def car_exit(request):
    try:
        parking = Parking.objects.first()
        if parking.available_spaces < parking.total_spaces:
            parking.available_spaces += 1
            parking.save()
        data = {
            'available_spaces': parking.available_spaces,
            'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')  # Formatear la fecha en el servidor
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error updating parking info: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)