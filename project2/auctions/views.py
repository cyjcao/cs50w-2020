from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Bid, Category, Comment, Listing, User
from .forms import ListingForm


def index(request):
    active_listings = Listing.objects.filter(is_active=True).order_by('-date_created')
    return render(request, "auctions/index.html", {
        "heading": "Active Listings",
        "listings": active_listings
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

def listing(request, listing_id):
    # Ensure listing exists
    try:
        listing = Listing.objects.get(pk=listing_id)
        bids = listing.bids.order_by('-amount', '-id')
        winning_bidder = True if bids.first().bidder and bids.first().bidder.username == request.user.username else False
        num_bids = len(bids) - 1
        on_watchlist = True if listing in User.objects.get(username=request.user.username).watchlist.all() else False
    except Listing.DoesNotExist:
        pass
    
    comments = Comment.objects.filter(listing=listing)
    success_message = ""

    # Perform different actions depending on which button was clicked
    if request.method == "POST" and 'submit-bid' in request.POST:
        pending_bid = float(request.POST['bid'])
        # Ensure bid is higher than current price
        if pending_bid > bids.first().amount or (bids.first().bidder is None and pending_bid == bids.first().amount):
            bid = Bid(bidder=request.user, listing=listing, amount=pending_bid)
            bid.save()
            num_bids += 1
            winning_bidder = True
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "num_bids": num_bids,
                "winning_bidder": winning_bidder,
                'on_watchlist': on_watchlist,
                "success_message": "Successfully placed bid.",
                "comments": comments
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "num_bids": num_bids,
                "winning_bidder": winning_bidder,
                'on_watchlist': on_watchlist,
                "error_message": "Bid is too low.",
                "comments": comments
            })
    elif request.method == "POST" and 'close-listing' in request.POST:
        listing.is_active = False
        listing.save()
        success_message = "Successfully closed listing."
    elif request.method == "POST" and 'add-watchlist' in request.POST:
        user = User.objects.get(username=request.user.username)
        user.watchlist.add(listing)
        user.save()
        on_watchlist = True
        success_message = "Added listing to watchlist"
    elif request.method == "POST" and 'remove-watchlist' in request.POST:
        user = User.objects.get(username=request.user.username)
        user.watchlist.remove(listing)
        user.save()
        on_watchlist = False
        success_message = "Removed listing from watchlist"

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "num_bids": num_bids,
        "winning_bidder": winning_bidder,
        'on_watchlist': on_watchlist,
        "success_message": success_message,
        "comments": comments
    })

def watchlist(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "auctions/index.html", {
        "heading": "Watchlist",
        "listings": user.watchlist.all()
    })

def categories(request):
    categories = Category.objects.order_by("category")
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/index.html", {
        "heading": category.category,
        "listings": category.listings.filter(is_active=True)
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            starting_bid = form.cleaned_data['starting_bid']
            new_listing = form.save(commit=False)
            new_listing.user_created = request.user
            new_listing.save()
            bid = Bid(listing=new_listing, amount=starting_bid)
            bid.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = ListingForm()
    
    return render(request, "auctions/new.html", {
        "form": form
    })

@require_http_methods(["POST"])
@login_required
def add_comment(request, listing_id):
    content = request.POST['comment']
    listing = Listing.objects.get(pk=listing_id)
    comment = Comment(content=content, user=request.user, listing=listing)
    comment.save()

    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))