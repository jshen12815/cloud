# Social actions for clouddj
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html', {})

@login_required
def create_playlist(request):
	if request.method == 'GET':
		form = CreatePlaylistForm()
	else:
		form = CreatePlaylistForm(request.POST)
		if form.is_valid():
			new_playlist = Playlist(profile=get_object_or_404(Profile, user=request.user), 
				name=form.cleaned_data['name'])
			new_playlist.save()

			# NEED TO UPDATE THIS LATER
			return render(request, 'home.html', {})

	# THIS TOO
	render(request, 'home.html', {})

def stream(request):
	return render(request, 'home.html', {})