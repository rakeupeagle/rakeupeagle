# Django
from django.contrib import admin


class IsAssignedFilter(admin.SimpleListFilter):
    title = 'Is Assigned'
    parameter_name = 'is_assigned'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(assignments__isnull=False)
        elif value == 'No':
            return queryset.exclude(assignments__isnull=False)
        return queryset
