from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListingForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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

@login_required
def create_listing(request):
    form = None

    if request.method == "POST":
        form = ListingForm(request.POST)
        
        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.user = request.user
            newListing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def validate_bid(first_bid, current_price, bid_price):
    if first_bid:
        if bid_price < current_price:
            return False
    else:
        if bid_price <= current_price:
            return False

    return True


def listing(request, id):
    page_listing = get_object_or_404(Listing, pk=id)
    is_in_watchlist = page_listing.watchlist_user.filter(pk=request.user.id).exists()
    owner = page_listing.user == request.user
    winner = page_listing.winner == request.user
    # print(owner)
    bids = page_listing.bids.all()

    if request.method == "POST":
        bid_price = request.POST["bid"]
        bid_price = float(bid_price)
        current_price = page_listing.price if page_listing.price else page_listing.start_bid
        first_bid = page_listing.price is None

        if not validate_bid(first_bid, current_price, bid_price):
            return render(request, "auctions/listing.html", {
                "listing": page_listing,
                "is_in_watchlist": is_in_watchlist,
                "message": "Invalid bid",
                "owner": owner,
                "winner": winner,
            })

        new_bid = Bid(user=request.user, listing=page_listing, price=bid_price)
        new_bid.save()
        page_listing.price = bid_price
        page_listing.save()
    
    #print(page_listing.active)

    return render(request, "auctions/listing.html", {
        "listing": page_listing,
        "is_in_watchlist": is_in_watchlist,
        "bids": len(bids),
        "owner": owner,
        "winner": winner,
        "active": page_listing.active,
        "comments": page_listing.comments.all()
    })

@login_required
def remove_watchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing.watchlist_user.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def add_watchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing.watchlist_user.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def close_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    if request.user == listing.user:
        listing.active = False
        listing.winner = listing.bids.order_by("-price").first().user
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def comments(request, id):
    listing = get_object_or_404(Listing, pk=id)

    if request.method == "POST":
        comment = request.POST["comment"]
        new_comment = Comment(user=request.user, listing=listing, comment=comment)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist_listings.all()
    })  

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.objects.values_list("category", flat=True).distinct()
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=category),
        "category": category
    })
