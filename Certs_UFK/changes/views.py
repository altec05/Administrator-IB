from django.shortcuts import render
from .models import Version, ChangeLog


def changes_list(request):
    versions = Version.objects.all().filter(visibility=True).order_by('-date_of_update')
    changes = versions
    print(changes)
    # changes = []
    # for version in versions:
    #     log = ChangeLog.objects.get(version=version)
    #     if log:
    #         changes.append([version.version, log.changes])

    return render(request, 'changes/changes_list.html', {'changes': changes})
