import main.models
from django.contrib.auth.models import User


class DB_Tools:
    @staticmethod
    def clear_table_of_model(model):
        model.objects.all().delete()