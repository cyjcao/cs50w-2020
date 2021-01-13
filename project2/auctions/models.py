from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

    def __str__(self):
        return f"Username: {self.username}"

class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=260)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="listings", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_listings')
    is_active =  models.BooleanField(default=True)

    def __str__(self):
        return f"Listing {self.id}: {self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        if self.bidder is None:
            return f"Starting bid of {self.amount} on {self.listing.title}"
        return f"{self.bidder.username} bid {self.amount} on {self.listing.title}"

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.listing.title}"

