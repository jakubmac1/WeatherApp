from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=pl&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    err_msg = ''
    message = ''
    message_class = ''
    del_msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Miasto nie istnieje.'

            else:
                err_msg = 'Miasto zostało już dodane.'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Miasto dodane.'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data =[]

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'humidity': r['main']['humidity'],
        }

        weather_data.insert(0,city_weather)

    context = {
        'weather_data': weather_data, 'form':form,
        'form': form,
        'message': message,
        'message_class': message_class,
    }
    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')