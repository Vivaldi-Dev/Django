from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# Definindo o validador alphanumeric se ainda não estiver definido.
alphanumeric = RegexValidator(
    r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
)


class Showroomlist(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassinumber = models.CharField(
        max_length=100, blank=True, null=True, validators=[alphanumeric]
    )
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey(
        Showroomlist, on_delete=models.CASCADE, related_name="cars", null=True
    )

    def __str__(self):
        return self.name

class Review(models.Model):
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(5)  
        ]
    )
    comments = models.CharField(max_length=200, null=True)
    car = models.ForeignKey(
        carlist, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Review for {self.car.name} with rating {self.rating}"

