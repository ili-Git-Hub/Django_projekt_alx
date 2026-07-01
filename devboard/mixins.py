from django.contrib.auth.mixins import LoginRequiredMixin

# from devboard.models import Project


class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Mixin, który filtruje queryset, aby zwracał tylko obiekty należące do zalogowanego użytkownika.
    """
    owner_field = "owner"

    def get_queryset(self):
        # return Project.objects.filter(owner=self.request.user)

        return super().get_queryset().filter(**{self.owner_field: self.request.user})
        # ** to wypakowanie słownika
