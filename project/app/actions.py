from django.contrib import admin


@admin.action(description="Invite Recipients/Teams")
def invite_instances(modeladmin, request, queryset):
    for instance in queryset:
        instance.invite()
        instance.save()


@admin.action(description="Ignore Recipients/Teams")
def ignore_instances(modeladmin, request, queryset):
    for instance in queryset:
        instance.ignore()
        instance.save()


@admin.action(description="Mark as Read")
def mark_read(modeladmin, request, queryset):
    for instance in queryset:
        instance.read()
        instance.save()


@admin.action(description="Send Message")
def send_message(modeladmin, request, queryset):
    for instance in queryset:
        instance.send()
        instance.save()
