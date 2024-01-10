from .models import Version


def add_variable_to_context(request):
    version = Version.objects.all().filter(visibility=True).order_by('-date_of_update').first()

    return {
        'version': version,
    }