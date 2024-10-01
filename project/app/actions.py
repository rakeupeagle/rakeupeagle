from django.contrib import admin


@admin.action(description="Send Invitations")
def send_invitations(modeladmin, request, queryset):
    for instance in queryset:
        instance.invite()
        instance.save()


@admin.action(description="Mark as Read")
def mark_read(modeladmin, request, queryset):
    for instance in queryset:
        instance.read()
        instance.save()
