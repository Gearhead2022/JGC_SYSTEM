from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from myapp.models import Events

from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

def crudevents(request):
    events = Events.objects.all()

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "addEvent":
            event_id = request.POST.get("event_id")
            title = request.POST.get("event_title")
            category = request.POST.get("category")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")

            try:
                if Events.objects.filter(event_id=event_id).exists():
                    return JsonResponse({'success': False, 'error_message': f"Event with event_id '{event_id}' already exists."})

                Events.objects.create(
                    event_id=event_id,
                    title=title,
                    category=category,
                    start_date = start_date,
                    end_date = end_date,
                    start_time = start_time,
                    end_time = end_time,
                    cottage='ambot',
                    room='ambotman'
                )
                return JsonResponse({'success': True})

            except IntegrityError as e:
                return JsonResponse({'success': False, 'error_message': str(e)})
            
        elif action == "editEvent":
            
            event_id = request.POST.get("event_id")
            title = request.POST.get("event_title")
            category = request.POST.get("category")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")

            try:
                events = Events.objects.get(event_id=event_id)
                events.title = title
                events.category = category
                events.start_date = start_date
                events.end_date = end_date
                events.start_time = start_time
                events.end_time = end_time

                events.save()
                return JsonResponse({'success': True})
            except Events.DoesNotExist:
                return JsonResponse({'success': False, 'error_message': f"Event with Event Code '{event_id}' does not exist."})

        elif action == "deleteEvent":
            event_code = request.POST.get("event_id_delete")
            try:
                events = Events.objects.get(event_id=event_code)
           
                events.delete()
                return JsonResponse({'success': True})
            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'error_message': 'Employee not found.'})

    return render(request, 'myapp/modules/nah.html', {'events': events})

def get_events(request):
    category = request.GET.get('category')
    if category:
        events = Events.objects.filter(category=category)
    else:
        events = Events.objects.all()
    
    events_data = []
    for event in events:
        try:
            start_time = datetime.strptime(event.start_time, '%H:%M').strftime('%H:%M') if event.start_time else None
            end_time = datetime.strptime(event.end_time, '%H:%M').strftime('%H:%M') if event.end_time else None

            event_data = {
                'title': event.title,
                'start': event.start_date.strftime('%Y-%m-%d') + ('T' + start_time if start_time else ''),
                'end': event.end_date.strftime('%Y-%m-%d') + ('T' + end_time if end_time else ''),
                'category': event.category,
                'event_id': event.event_id,
                'start_time': event.start_time,
                'end_time': event.end_time,
            }

            events_data.append(event_data)

        except ValueError as e:
            print(f"Error parsing time for event {event.event_id}: {e}")

    return JsonResponse(events_data, safe=False)

def nah(request):
    return render(request, 'myapp/modules/nah.html')

# def checkwriter(request):
#     return render(request, 'myapp/checkwriter.html')

@csrf_exempt
def get_next_event_id(request):
    if request.method == 'GET':
        try:
            last_event = Events.objects.latest('id')
            last_id = last_event.id
        except Events.DoesNotExist:
            last_id = 0
        next_event_code = f'EV-{last_id + 1:04d}'
        return JsonResponse({'next_event_code': next_event_code})
    return JsonResponse({'error': 'Invalid request'}, status=400)