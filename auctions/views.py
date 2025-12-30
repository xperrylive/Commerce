from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.db.models import Max
from decimal import Decimal

from .models import User,AuctionListing,Comment,Category
from .forms import CreateListingForm



def index(request):
    auctions_list = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"auctions_list":auctions_list})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing_view(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    comments = listing.comments.all()
    highest_bid = listing.bids.order_by("-bid_amount").first()
    error = None

    if highest_bid == None:
        current_price = listing.starting_bid
    else:
        current_price = highest_bid.bid_amount

    if request.method == "POST":
        try:
            offer = Decimal(request.POST["bid_amount"])
        except ValueError:
            error = "Bid Amount must be a Number"
            return render(request, "auctions/listing.html", {
                "listing":listing, 
                "comments":comments, 
                "current_price": current_price,
                "highest_bidder": highest_bid.user.username if highest_bid else None,
                "min_bid":current_price + Decimal("0.01"), 
                "error": error})

        if offer > current_price:
            # django automatically fills the listing field
            listing.bids.create(user=request.user, bid_amount=offer)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            error = f"Bid must be higher than ${current_price}"
    
    return render(request, "auctions/listing.html", {
        "listing":listing, 
        "comments":comments, 
        "current_price": round(current_price,2),
        "highest_bidder": highest_bid.user.username if highest_bid else None,
        "min_bid":current_price + Decimal("0.01"), 
        "error": error})


@login_required(login_url="login")
def watchlist_toggle(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if  listing.watched_by.filter(pk=request.user.pk).exists():
        listing.watched_by.remove(request.user)
    else:
        listing.watched_by.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="login")
def close_auction(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        user = request.user

        if user != listing.owner:
            return HttpResponseRedirect(reverse("index"))
        
        highest_bid = listing.bids.order_by("-bid_amount").first()
        
        if highest_bid:
            listing.winner = highest_bid.user
        
        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("index"))

def create_listing_view(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
    return render(request,"auctions/create_listing.html", {"form":form})

@login_required(login_url="login")
def watchlist_view(request):
    user = request.user
    watchlist = user.watch_list.filter(is_active=True)
    return render(request,"auctions/watchlist.html", {"auctions_list":watchlist})



@login_required(login_url="login")
def add_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment_content"]
        user = request.user
        
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        Comment.objects.create(
            user=user,
            listing=listing,
            content=comment)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def category_list(request):
    categories_list = Category.objects.all()
    return render(request,"auctions/categories.html",{"categories_list": categories_list})

def listing_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = AuctionListing.objects.filter(is_active=True, category=category)
    
    return render(request,"auctions/index.html",{
        "auctions_list": listings,
        "title": f"{category.name} Listings"
    })