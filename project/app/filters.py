from django.contrib.admin import SimpleListFilter


class DirectionListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Direction'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "direction"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        values = [
            ('inbound', 'Inbound'),
            ('outbound', 'Outbound'),
        ]

        return values

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'outbound':
            return queryset.filter(
                author__isnull=True,
            )
        elif self.value() == 'inbound':
            return queryset.filter(
                author__isnull=False,
            )
