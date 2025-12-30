from django.contrib import admin
from .models import AuctionListing,Comment,Category,Bid,User

# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ["id","title","owner","starting_bid","is_active"]

class UserAdmin(admin.ModelAdmin):
    # This makes the ManyToMany selection much better
    filter_horizontal = ("watch_list",)

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(User, UserAdmin)
