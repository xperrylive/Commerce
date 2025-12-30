from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watch_list = models.ManyToManyField("AuctionListing", blank=True, related_name="watched_by")


class AuctionListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    image_url = models.URLField(blank=True)
    starting_bid = models.DecimalField(max_digits=10 ,decimal_places=2)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="won_listings",blank=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, )
    listing = models.ForeignKey(AuctionListing,  on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"User:{self.user} Bid Amount:{self.bid_amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)

    def __str__(self):
        return self.content