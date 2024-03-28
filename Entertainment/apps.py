
from django.apps import AppConfig


class EntertainmentConfig(AppConfig):
    """
    AppConfig for the "Entertainment" app.

    Attributes:
        name (str): The name of the app ("Entertainment").
        default_auto_field (str): The default auto field for model primary keys (BigAutoField).

    Example:
        To use this AppConfig in your Django project, add the following to your project's settings.py:

        .. code-block:: python

            INSTALLED_APPS = [
                # ...
                "Entertainment",
                # ...
            ]
    """
    name = "Entertainment"
    default_auto_field = "django.db.models.BigAutoField"
