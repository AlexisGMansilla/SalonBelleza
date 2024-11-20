
from .models import Cliente

def client_count(request):
    return {
        'client_count': Cliente.objects.count()
    }
