from django.db import models

from django.contrib.auth.models import User
User.add_to_class('is_seller', models.BooleanField(default=False))