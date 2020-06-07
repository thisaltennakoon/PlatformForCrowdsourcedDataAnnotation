import django_filters
from .models import Profile

class ProfileFilter (django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['first_name', 'is_contributor', 'is_author']



