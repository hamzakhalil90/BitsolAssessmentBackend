from django.db import models


class LogsMixin(models.Model):
    """Add the generic fields and relevant methods common to support mostly
    models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        """metaclass for LogsMixin"""

        abstract = True
