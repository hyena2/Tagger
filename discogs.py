import sys
import discogs_client
from discogs_client.exceptions import HTTPError
import eyed3

consumer_key = 'mwGOWlfNuWhbUDYWuQTX'
consumer_secret = 'BbCirdZVwQjMhZGgySwmkgqoTCHFvaQu'
user_agent = 'Tagger'

discogsclient = discogs_client.Client(user_agent)

discogsclient.set_consumer_key(consumer_key, consumer_secret)
token, secret, url = discogsclient.get_authorize_url()

print ' == Request Token == '
print '    * oauth_token        = {0}'.format(token)
print '    * oauth_token_secret = {0}'.format(secret)
print

print 'Please browse to the following URL {0}'.format(url)

accepted = 'n'
while accepted.lower() == 'n':
    print
    accepted = raw_input('Have you authorized me at {0} [y/n] :'.format(url))


oauth_verifier = raw_input('Verification code :').decode('utf8')

try:
    access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
except HTTPError:
    print 'Unable to authenticate.'
    sys.exit(1)

user = discogsclient.identity()

print
print ' == User =='
print '    * username           = {0}'.format(user.username)
print ' == Access Token =='
print '    * oauth_token        = {0}'.format(access_token)
print '    * oauth_token_secret = {0}'.format(access_secret)
print ' Authentication complete. Future requests will be signed with the above tokens.'

print "File"
file_ = raw_input()
audiofile = eyed3.load(file_)
print "Artist"
artist = raw_input()
print "Song"
song = raw_input()

while artist != "exit":
	search_results = discogsclient.search(song, type='release',
		artist=artist)

	for release in search_results:
		    print '\n\t== discogs-id {id} =='.format(id=release.id)
		    print u'\tArtist\t: {artist}'.format(artist=', '.join(artist.name for artist
							 in release.artists))
		    print u'\tTitle\t: {title}'.format(title=release.title)
		    print u'\tYear\t: {year}'.format(year=release.year)
		    print u'\tLabels\t: {label}'.format(label=','.join(label.name for label in
							release.labels))

		    count = 0
		    for track in release.tracklist:
		    	    print count
			    print track.title
			    count = count + 1

		    print "Press Y if you those tags are correct, press N to keep on searching"
		    answer = raw_input()
	    
		    if answer == "y":
		    	    print "Which is the track ou are looking for?"
			    trackNumber = int(raw_input())
			    audiofile.tag.title = release.tracklist[trackNumber].title
			    audiofile.tag.album = release.title
			    audiofile.tag.year = release.year
			    audiofile.tag.save()
			    break

	print "Next file"
        file_ = raw_input() 
	print "Artist"
	artist = raw_input()
	print "Song"
	song = raw_input()
