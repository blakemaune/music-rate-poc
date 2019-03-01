from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Rating, Album
from .forms import SearchForm, SearchResult, RatingForm
import requests
import json

# Create your views here.
def ratings_list(request):
	ratings = Rating.objects.all().order_by('-updated')
	return render(request, 'myApp/ratings.html', {'ratings':ratings})

def get_json(query):
	getTokenData={
		"client_id":"d3fb423d78d6479a9ab409baccd10cc2",
		"client_secret":"691f84aaf05a41528a916f96c33f4416",
		"grant_type":"client_credentials"
	}
	r = requests.post(url = "https://accounts.spotify.com/api/token", data=getTokenData)
	token_json = r.text
	parsed_json = json.loads(token_json)
	token = parsed_json["access_token"]
	stem = "https://api.spotify.com/v1/search?q="
	
	print("QUERYING SPOTIFY WITH " + stem+query)
	headers = {"Authorization": "Bearer " + token}
	q = requests.get(url = stem+query, headers=headers)
	response = q.text
	return json.loads(response)

def search_form(request):
	print(request)
	if request.method == "POST":
		#DO stuff
		form = SearchForm(request.POST)
		if form.is_valid():
			artist = request.POST['artist']
			name = request.POST['name']
			query = ""
			if name is not "":
				query += "album%3A" + name
			if artist is not "":
				query += "%20artist%3A" + artist
			query += "&type=album"
			print("Got NAME="+name+" and ARTIST="+artist)
			parsedAlbums=get_json(query)
			results = []
			for album in parsedAlbums['albums']['items']:
				result = {'name':album['name'],'artist':album['artists'][0]['name'], 'id':album['id'], 'img':album['images'][0]['url']}
				results.append(result)
			return render(request, 'myapp/search_result.html', {'results':results, 'og_data':parsedAlbums['albums']['items']})
			# data = json.dumps(parsedAlbums['albums']['items'])
			# return render(request, 'myapp/search_result.html', {'data':data})
	else:
		form = SearchForm()
		return render(request, 'myapp/search_form.html', {'form':form})

def rating_detail(request, ratingID):
	rating = Rating.objects.get(id=ratingID)
	return render(request, 'myApp/rating_detail.html', {'rating':rating})

# V2 Notes
# When create/edit a rating
# INPUT: Spotify URI
# 	IF album exists
# 		IF rating exists
# 			go straight to rating ID
# 		IF rating doesnt exist
# 			create rating
# 			refresh, sending new rating ID
# 	IF album doesnt exist
# 		create album
# 		refresh, sending album URI
# INPUT: Rating ID
# 	go straight to rating ID
	
def rating_edit(request, ratingID=None, uri=None):
	# If uri is none, ratingID is not none
	# This means we have a ratingID
	# This means we have a rating
	# View an existing rating
	if uri is None:
		rating = Rating.objects.get(id=ratingID)
		if(request.user == rating.user):
			if request.method == "POST":
				print("Got a post request, rating is: " + str(rating))
				form = RatingForm(request.POST, instance=rating)
				if form.is_valid():
					rating = form.save(commit=False)
					rating.updated = timezone.now()
					rating.save()
					return redirect('rating_detail', ratingID=rating.pk)
			print("You created this rating!")
			form = RatingForm({'user':rating.user, 'album':rating.album, 'value':rating.value, 'comment':rating.comment, 'updated':rating.updated})
			return render(request, 'myApp/rating_edit.html', {'form':form, 'rating':rating})
		else:
			print("You didn't create this rating!")
			return redirect('rating_detail', ratingID=ratingID)

	elif ratingID is None:
		album = Album.objects.get(spotify_id=uri)
		rating, created = Rating.objects.get_or_create(album=album, user=request.user)
		return redirect(rating_edit, ratingID=rating.id)
	
# def rating_edit(request, uri):
# 	album = Album.objects.get(spotify_id=uri)
# 	rating, created = Rating.objects.get_or_create(album=album, user=request.user)
# 	return redirect(rating_edit, ratingID=rating.id)


# WE SHOULD NOT CREATE AN ALBUM RECORD ON VIEW!
# Need to replace the {'album': album}
# Instead of passing model to template
# V2 should pass dict to template
def album_detail(request, uri):
	album, created = Album.objects.get_or_create(spotify_id=uri)
	if created is True:
		print("Creating a new album!")
		album.name = request.GET['name']
		album.artist = request.GET['artist']
		album.art_url = request.GET['img']
		album.save()
		#Display detail view
		return redirect('/album/'+uri)
		#return redirect('album_detail', uri=uri)
	elif created is False and len(request.GET)!=0:
		print("Still getting get parameters. Need to redirect you")
		return redirect("/album/"+uri+"/")
	ratings = Rating.objects.filter(album=album.spotify_id)
	return render(request, 'myApp/album_detail.html', {'album':album, 'ratings':ratings})
	
