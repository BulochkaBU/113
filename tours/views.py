from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
import random
from tours import data


# Create your views

def main_view(request):
    random_title_hotels_dict = dict(random.sample(data.tours.items(), 6))
    return render(request, 'index.html', context={
        'title': data.title,
        'subtitle': data.subtitle,
        'description': data.description,
        'departures': data.departures,
        'hotel_title': random_title_hotels_dict,
    })


def departure_view(request, departure):
    dep = data.departures[departure]
    tours = data.tours
    nights, prices = [], []
    dep_tours = {}
    count_tour = 0
    for key, value in tours.items():
        if value['departure'] == departure:
            dep_tours[key] = value
            nights.append(value['nights'])
            prices.append(value['price'])
            count_tour += 1
    min_nights = min(nights)
    max_nights = max(nights)
    min_price = min(prices)
    max_price = max(prices)
    return render(request, 'departure.html', context={
        'departure': dep,
        'dep_tours': dep_tours,
        'count_tour': count_tour,
        'min_nights': min_nights,
        'max_nights': max_nights,
        'min_price': min_price,
        'max_price': max_price,
    })


def tour_view(request, tour_id):
    tour = data.tours[tour_id]
    tour_departure = data.departures[tour['departure']]
    stars = int(tour['stars'])
    for star in range(stars + 1):
        star *= '★'
    return render(request, 'tour.html', context={
        'tour': tour,
        'tour_departure': tour_departure,
        'star': star,
    })


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
