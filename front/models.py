from django.db import models

class Gallery(models.Model):
    IN_HOME_PAGE = 1
    IN_TOP = 2
    DEFAULT = 0
    POSITION_CHOICES = (
        (IN_HOME_PAGE, 'Home Gallery'),
        (IN_TOP, 'Top Achievements'),
        (DEFAULT, 'Default'),
    )
    image = models.ImageField(upload_to = 'images/gallery/')
    position = models.PositiveSmallIntegerField(choices=POSITION_CHOICES, default=DEFAULT)


class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()