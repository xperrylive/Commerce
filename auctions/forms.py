from django.forms import ModelForm
from .models import AuctionListing


class CreateListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title","description","image_url", "starting_bid", "category"]
