def metadata(request):
    return {
        'author': 'Jacek Kowalski',
        'company': 'Drzewniane.pl',
        'ip_address': request.META['REMOTE_ADDR']
    }