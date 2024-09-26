from django.contrib import admin


@admin.action(description="Send Invitations")
def send_invitations(modeladmin, request, queryset):
    for instance in queryset:
        instance.invite()
        instance.save()
