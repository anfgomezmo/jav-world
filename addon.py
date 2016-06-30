import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
from lxml.html import parse, tostring
import xbmc, os, xbmcaddon

__addon__ = xbmcaddon.Addon(id='plugin.video.javworld')
__addondir__ = xbmc.translatePath( __addon__.getAddonInfo('path') ) #path/profile
__url__ = sys.argv[0] 				# Get the plugin url in plugin:// notation.
__handle__ = int(sys.argv[1]) 		# Get the plugin handle as an integer number.

_BEJAV = '0'
_VJAV = '1'
_JAVHIHI = '2'
_JAV789 = '3'
_JAPANESEPORN18 = '4'
_JAVSTREAMS = '5'
_YOUJAV = '6'
_JAVSEX = '7'
_JAVONLINE = '8'
_NEW = '9'


webs = [('Bejav', 'http://animeflv.net/'),
		('vjav', 'http://www.animeid.tv/'),
		('javhihi', 'http://jkanime.net/'),
		('jav789', 'http://jkanime.co/'),
		('japaneseporn18', 'http://elanimeonline.com/'),
		('javstreams', 'http://www.fullanimes.net/'),
		('youjav', 'http://animeflv.me/'),
		('javsex', 'http://animeflv.me/'),
		('javonline', 'http://www.animeyt.tv/')]



def search(site):
	keyboard = xbmc.Keyboard("", "Type your name", False)
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText() != "":
		if site == _BEJAV:
			url = 'http://bejav.com/search/' + keyboard.getText()
		elif site == _VJAV:
			url = 'http://www.vjav.com/search/' + keyboard.getText() +'/'
		elif site == _JAVHIHI:
			url = 'http://javhihi.com/movie?q=' + keyboard.getText()
		elif site == _JAV789:
			url = 'http://jav789.com/movie?q=' + keyboard.getText()
		elif site == _JAPANESEPORN18:
			url = 'http://www.japaneseporn18.com/?s=' + keyboard.getText()
		elif site == _JAVSTREAMS:
			url = 'http://bejav.com/search/' + keyboard.getText()
		elif site == _YOUJAV:
			url = 'http://bejav.com/search/' + keyboard.getText()
		elif site == _JAVSEX:
			url = 'http://bejav.com/search/' + keyboard.getText()
		elif site == _JAVONLINE:
			url = 'http://www.javonline.me/show/' + keyboard.getText()

		list_videos(url, site)


#########################################
#				LIST VIDEOS				#
#########################################

def list_videos_bejav(link):
	html = parse(link).getroot()
	listing = []
	for video in html.cssselect('#content-main > div > div.wrap-tab > div:nth-child(n+1) > div.thumb > a'):
		link = video.attrib['href']
		title = video.attrib['title']
		image = video.cssselect('img')
		image_src = image[0].attrib['src']

		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image_src)
		list_item.setInfo('video', {'title': title, 'genre': title})
		list_item.setProperty('IsPlayable', 'true')


		url = '{0}?action=play&link={1}&site={2}'.format(__url__, link, _BEJAV)
		is_folder = False
		listing.append((url, list_item, is_folder))


	# NEXT PAGE
	pl = html.cssselect('#content-main > div > div.wrap-tab > div.c-pagination.text-center > ul > li:nth-last-child(1) > a')

	if pl:
		page = pl[0].attrib['href']
		image = 'Default.png'
		list_item = xbmcgui.ListItem(label='Next page', thumbnailImage=image)
		list_item.setInfo('video', {'title': 'Next page'})
		url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, page, _BEJAV)
		is_folder = True
		listing.append((url, list_item, is_folder))

	return listing

def list_videos_vjav(link):
	root = parse(link).getroot()
	listing = []
	elements =	root.cssselect('#list_videos_common_videos_list_items > div > a')
	elements = elements + root.cssselect('#list_videos_latest_videos_list_items > div > a')
	elements = elements + root.cssselect('#list_videos_videos_list_search_result_items > div > a')

	for div in elements:
		title = div.attrib['title']
		link = div.attrib['href']
		img = div.cssselect('div > img')
		image = img[0].attrib['data-original']

		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image)
		#list_item.setProperty('fanart_image', video[2])
		list_item.setInfo('video', {'title': title, 'genre': title})
		list_item.setProperty('IsPlayable', 'true')

		url = '{0}?action=play&link={1}&site={2}'.format(__url__, link, _VJAV)
		is_folder = False
		listing.append((url, list_item, is_folder))

	return listing


def list_videos_javhihi(link):
	root = parse(link).getroot()
	listing = []
	xbmc.log('I AM AT: ' + link)
	for div in root.cssselect('body > div.main > div.main-page > div:nth-child(2) > div > div.movie-list > div > div > div.item-thumbnail > a'):
		title = div.attrib['title']
		link = 'http://javhihi.com/' + div.attrib['href']
		img = div.cssselect('img')
		image = img[0].attrib['src']
		
		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image)			
		list_item.setInfo('video', {'title': title, 'genre': title})		
		list_item.setProperty('IsPlayable', 'true')
		
		url = '{0}?action=play&link={1}&site={2}'.format(__url__, link, _JAVHIHI)	
		is_folder = False		
		listing.append((url, list_item, is_folder))
	
	p = root.cssselect('body > div.main > div.main-page > div:nth-child(2) > div > center > a')
	if p:
		page = 'http://javhihi.com/' + p[0].attrib['href']
		xbmc.log('GO TO: ' + page)
		list_item = xbmcgui.ListItem(label='Next page', thumbnailImage='Default.png')			
		url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, page, _JAVHIHI)
		is_folder = True		
		listing.append((url, list_item, is_folder))
	
	return listing

def list_videos_jav789(link):
	root = parse(link).getroot()
	listing = []
	xbmc.log('I AM AT: ' + link)
	for div in root.cssselect('body > div.main > div.main-page > div:nth-child(2) > div > div.movie-list > div > div > div.item-thumbnail > a'):
		title = div.attrib['title']
		link = 'http://jav789.com/' + div.attrib['href']
		img = div.cssselect('img')
		image = img[0].attrib['src']
		
		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image)			
		list_item.setInfo('video', {'title': title, 'genre': title})		
		list_item.setProperty('IsPlayable', 'true')
		
		url = '{0}?action=play&link={1}&site={2}'.format(__url__, link, _JAV789)	
		is_folder = False		
		listing.append((url, list_item, is_folder))
	
	p = root.cssselect('body > div.main > div.main-page > div:nth-child(2) > div > center > a')
	if p:
		page = 'http://jav789.com/' + p[0].attrib['href']
		xbmc.log('GO TO: ' + page)
		list_item = xbmcgui.ListItem(label='Next page', thumbnailImage='Default.png')			
		url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, page, _JAV789)
		is_folder = True		
		listing.append((url, list_item, is_folder))
	
	return listing
	

def list_videos_japaneseporn18(link):

	root = parse(link).getroot()
	listing = []

	for div in root.cssselect('#content > div.box > div > a'):
		link = div.attrib['href']
		title = div.attrib['title'].strip('Permanent Link to ')
		img = div.cssselect('img')
		image = 'http://www.japaneseporn18.com' + img[0].attrib['src']

		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image)
		#list_item.setProperty('fanart_image', video[2])
		list_item.setInfo('video', {'title': title, 'genre': title})
		list_item.setProperty('IsPlayable', 'true')

		url = '{0}?action=play&link={1}&site={2}'.format(__url__, link, _JAPANESEPORN18)
		is_folder = False
		listing.append((url, list_item, is_folder))

	#NEXTPAGE
	pl = root.cssselect('#navigation > div > a.nextpostslink')
	if pl:
		page = pl[0].attrib['href']
		image = 'Default.png'
		list_item = xbmcgui.ListItem(label='Next page', thumbnailImage=image)
		list_item.setProperty('fanart_image', image)
		list_item.setInfo('video', {'title': 'Next page'})
		url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, page, _JAPANESEPORN18)
		is_folder = True
		listing.append((url, list_item, is_folder))

	return listing

#def list_videos_javstreams(link):
#def list_videos_youjav(link)
#def list_videos_javsex(link)

def list_videos_javonline(link):
	html = parse(link).getroot()
	listing = []
	for video in html.cssselect('#channel-content > div.loop-content > div > div.video-thumb > a.clip-link'):
		link = video.attrib['href']
		title = video.attrib['title']
		image = video.cssselect('img')
		image_src = image[0].attrib['src']

		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image_src)
		list_item.setInfo('video', {'title': title, 'genre': title})
		list_item.setProperty('IsPlayable', 'true')

		url = '{0}?action=play&link={1}&site={2}'.format(__url__, link, _JAVONLINE)
		is_folder = False
		listing.append((url, list_item, is_folder))
	return listing


def list_videos(link, site, page = None):
	if site == _BEJAV:
		listing = list_videos_bejav(link)
	elif site == _VJAV:
		listing = list_videos_vjav(link)
	elif site == _JAVHIHI:
		if not page == '0':
			link = link + '&page=' + page
		listing = list_videos_javhihi(link)
	elif site == _JAV789:
		if not page == '0':
			link = link + '&page=' + page
		listing = list_videos_jav789(link)
	elif site == _JAPANESEPORN18:
		listing = list_videos_japaneseporn18(link)
	elif site == _JAVSTREAMS:
		listing = list_videos_javstreams(link)
	elif site == _YOUJAV:
		listing = list_videos_youjav(link)
	elif site == _JAVSEX:
		listing = list_videos_javsex(link)
	elif site == _JAVONLINE:
		listing = list_videos_javonline(link)
	else:
		listing = []


	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))

	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.confluence':
		xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
	elif skin_used == 'skin.aeon.nox':
		xbmc.executebuiltin('Container.SetViewMode(512)') # "Info-wall" view.

	# Finish creating a virtual folder.
	xbmcplugin.endOfDirectory(__handle__)

#########################################
#				PLAY VIDEO				#
#########################################

def play_video_bejav(link):
	doc = parse(link).getroot()
	div = doc.cssselect('#content-main > div.col-xs-12.watch > div > div.player > script:nth-child(4)')
	url = tostring(div[0]).split('{file:"')[1].split('"}')[0]
	return url

def play_video_vjav(link):
	root = parse(link).getroot()
	div = root.cssselect('body > div.container > div.content > div.block-video > div.video-holder > div.player > div > script:nth-child(3)')
	url = tostring(div[0]).split("video_url: '")[1].split("'")[0]
	return url

def play_video_javhihi(link):
	root = parse(link).getroot()
	div = root.cssselect('#player > source:nth-child(1)')
	url = div[0].attrib['src']
	#url = 'https://15zf8e5.oloadcdn.net/dl/l/1T9bPb59iiU/e1iLJ6na-yg/STAR-690.avi.mp4'
	return url

def play_video_jav789(link):
	root = parse(link).getroot()
	div = root.cssselect('#player > source:nth-child(1)')
	url = div[0].attrib['src']
	return url

def play_video_japaneseporn18(link):
	root = parse(link).getroot()
	video = root.cssselect('#anc_pl > video > source')
	if video:
		url = video[0].attrib['src']
	else:
		iframe = root.cssselect('#anc_pl > iframe')
		url = 'http://www.japaneseporn18.com' + iframe[0].attrib['src']

		html = parse(url).getroot()
		video = html.cssselect('#anc_pl > video > source')
		url = video[0].attrib['src']
	return url


#def play_video_javstreams(link):
#def play_video_youjav(link):
#def play_video_javsex(link):

def play_video_javonline(link):
	link = str.replace(link, 'https', 'http')
	root = parse(link).getroot()
	div = root.cssselect('#video-content > div.video-player.pull-left.external > script')
	url = tostring(div[0]).split('"')[5]
	return url
	


def play_video(link, site):
	"""
	Play a video by the provided path.
	:param path: str
	:return: None
	"""

	if site == _BEJAV:
		url = play_video_bejav(link)
	elif site == _VJAV:
		url = play_video_vjav(link)
	elif site == _JAVHIHI:
		url = play_video_javhihi(link)
	elif site == _JAV789:
		url = play_video_jav789(link)
	elif site == _JAPANESEPORN18:
		url = play_video_japaneseporn18(link)
	elif site == _JAVSTREAMS:
		url = play_video_javstreams(link)
	elif site == _YOUJAV:
		url = play_video_youjav(link)
	elif site == _JAVSEX:
		url = play_video_javsex(link)
	elif site == _JAVONLINE:
		url = play_video_javonline(link)
	else:
		url = []

	#ink = 'https://content-na.drive.amazonaws.com/cdproxy/templink/v5bR3kSPPzb0BTgdEjP9c-f50-KN997Qg34-XISCY78LAYspN'
	play_item = xbmcgui.ListItem(path=url) # Create a playable item with a path to play.
	xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item) # Pass the item to the Kodi player.

#########################################
#			SITES (START)				#
#########################################

def list_sites():
	listing = []
	for idx, web in enumerate(webs):
		name = web[0]
		image = __addondir__ + '/images/'+str(idx)+'.png'
		#xbmc.log(image)
		#fanart = __addondir__ + '/fanart.jpg'

		list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
		#list_item.setProperty('fanart_image', fanart)
		list_item.setInfo('video', {'title': name, 'genre': name})
		url = '{0}?action=listsite&site={1}'.format(__url__, idx)
		is_folder = True

		listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE) # SORT
	xbmcplugin.endOfDirectory(__handle__) # Finish


#########################################
#				LIST SITES				#
#########################################

def list_bejav():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _BEJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#TOP JAV
	name = 'Top JAV'
	image = 'Default.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://bejav.com/top-jav/', _BEJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#JAV HOT
	name = 'JAV Hot'
	image = 'Default.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://bejav.com/jav-hot/', _BEJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _BEJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_vjav():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _VJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MODELS
	name = 'Models'
	image = __addondir__ + '/images/models.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listmodels&site={1}'.format(__url__, _VJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.vjav.com/latest-updates/', _VJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#TOP RATED
	name = 'Top Rated'
	image = __addondir__ + '/images/toprated.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.vjav.com/top-rated/', _VJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MOST VIEWED
	name = 'Most Viewed'
	image = __addondir__ + '/images/mostviewed.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.vjav.com/most-popular/', _VJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _VJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_javhihi():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _JAVHIHI)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MODELS
	name = 'Models'
	image = __addondir__ + '/images/models.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listmodels&site={1}'.format(__url__, _JAVHIHI)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, 'http://javhihi.com/movie', _JAVHIHI)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#TOP RATED
	name = 'Top Rated'
	image = __addondir__ + '/images/toprated.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, 'http://javhihi.com/movie?sort=likeweek', _JAVHIHI)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MOST VIEWED
	name = 'Most Viewed'
	image = __addondir__ + '/images/mostviewed.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, 'http://javhihi.com/movie?sort=viewweek', _JAVHIHI)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}&page=0'.format(__url__, _JAVHIHI)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_jav789():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _JAV789)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MODELS
	name = 'Models'
	image = __addondir__ + '/images/models.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listmodels&site={1}'.format(__url__, _JAV789)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, 'http://jav789.com/movie', _JAV789)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#TOP RATED
	name = 'Top Rated'
	image = __addondir__ + '/images/toprated.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, 'http://jav789.com/movie?sort=likeweek', _JAV789)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MOST POPULAR
	name = 'Most Popular'
	image = __addondir__ + '/images/mostviewed.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, 'http://jav789.com/movie?sort=viewweek', _JAV789)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}&page=0'.format(__url__, _JAV789)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_japaneseporn18():
	listing = []

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	fanart = __addondir__ + '/images/sakuraaida.jpg'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setProperty('fanart_image', fanart)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.japaneseporn18.com/', _JAPANESEPORN18)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	fanart = __addondir__ + '/images/facial.jpg'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setProperty('fanart_image', fanart)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _JAPANESEPORN18)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_javstreams():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _JAVSTREAMS)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _JAVSTREAMS)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#TOP RATED
	name = 'Top Rated'
	image = __addondir__ + '/images/toprated.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _JAVSTREAMS)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MOST VIEWED
	name = 'Most Viewed'
	image = __addondir__ + '/images/mostviewed.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _JAVSTREAMS)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _JAVSTREAMS)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_youjav():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _YOUJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _YOUJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#TOP RATED
	name = 'Top Rated'
	image = __addondir__ + '/images/toprated.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _YOUJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#MOST VIEWED
	name = 'Most Viewed'
	image = __addondir__ + '/images/mostviewed.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _YOUJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _YOUJAV)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_javsex():
	listing = []

	#CATEGORIES
	name = 'Categories'
	image = __addondir__ + '/images/categories.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listcategories&site={1}'.format(__url__, _JAVSEX)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#LATEST
	name = 'Latest'
	image = __addondir__ + '/images/latest.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, '#', _JAVSEX)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _JAVSEX)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish

def list_javonline():
	listing = []

	#CENSORED
	name = 'Censored'
	image = __addondir__ + '/images/censored.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.javonline.me/channel/censored/1/', _JAVONLINE)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#UNCENSORED
	name = 'Uncensored'
	image = __addondir__ + '/images/uncensored.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.javonline.me/channel/uncensored/2/', _JAVONLINE)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#THAI
	name = 'Thai'
	image = __addondir__ + '/images/thai.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.javonline.me/channel/porn-thai/3/', _JAVONLINE)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#WESTERN
	name = 'Western'
	image = __addondir__ + '/images/western.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, 'http://www.javonline.me/channel/western/4/', _JAVONLINE)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	#SEARCH
	name = 'Search'
	image = __addondir__ + '/images/search.png'
	list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
	list_item.setInfo('video', {'title': name, 'genre': name})
	url = '{0}?action=search&site={1}'.format(__url__, _JAVONLINE)
	is_folder = True
	listing.append((url, list_item, is_folder)) # ADD ELEMENT TO LIST

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))	# ADD DIRECTORIES
	xbmcplugin.endOfDirectory(__handle__) # Finish



def list_site(site):
	if site == _BEJAV:
		list_bejav()
	elif site == _VJAV:
		list_vjav()
	elif site == _JAVHIHI:
		list_javhihi()
	elif site == _JAV789:
		list_jav789()
	elif site == _JAPANESEPORN18:
		list_japaneseporn18()
	elif site == _JAVSTREAMS:
		list_javstreams()
	elif site == _YOUJAV:
		list_youjav()
	elif site == _JAVSEX:
		list_javsex()
	elif site == _JAVONLINE:
		list_javonline()
	else:
		list_sites()

#########################################
#				CATEGORIES				#
#########################################

def list_categories_bejav():
	image = 'Default.png'
	html = parse('http://bejav.com').getroot()
	listing = []
	for category in html.cssselect('#menu-sidebar-menu > li > a'):
		link = category.attrib['href']
		name = category.attrib['title']

		list_item = xbmcgui.ListItem(label=name, thumbnailImage=image)
		list_item.setInfo('video', {'title': name, 'genre': name})

		url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, link, _BEJAV)
		is_folder = True
		listing.append((url, list_item, is_folder))

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
	xbmcplugin.endOfDirectory(__handle__)

def list_categories_vjav():
	root = parse('http://www.vjav.com/categories/').getroot()

	listing = []
	for category in root.cssselect('#list_categories_categories_list_items > a'):
		link = category.attrib['href']
		title = category.attrib['title']
		img = category.cssselect('img')
		image = img[0].attrib['src']

		list_item = xbmcgui.ListItem(label=title, thumbnailImage=image)
		#list_item.setProperty('fanart_image', fanart)
		list_item.setInfo('video', {'title': title, 'genre': title})

		url = '{0}?action=listvideos&link={1}&site={2}'.format(__url__, link, _VJAV)
		is_folder = True
		listing.append((url, list_item, is_folder))

	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.endOfDirectory(__handle__)


def list_categories_javhihi():	
	root = parse('http://javhihi.com/').getroot()
	
	listing = []
	for category in root.cssselect('body > div.main > header > div > div.header-links.header-item > ul > li.dropdown > div > div > div > a'):
		link = 'http://javhihi.com/' + category.attrib['href']
		title = category.attrib['title']
		list_item = xbmcgui.ListItem(label=title, thumbnailImage='Default.png')
		list_item.setInfo('video', {'title': title, 'genre': title})

		url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, link, _JAVHIHI)
		xbmc.log(url)
		is_folder = True
		listing.append((url, list_item, is_folder))


	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.endOfDirectory(__handle__)
	

def list_categories_jav789():
	root = parse('http://jav789.com/').getroot()
	
	listing = []
	for category in root.cssselect('body > div.main > header > div > div.header-links.header-item > ul > li.dropdown > div > div > div > a'):
		link = 'http://jav789.com/' + category.attrib['href']
		title = category.attrib['title']
		list_item = xbmcgui.ListItem(label=title, thumbnailImage='Default.png')
		list_item.setInfo('video', {'title': title, 'genre': title})

		url = '{0}?action=listvideos&link={1}&site={2}&page=0'.format(__url__, link, _JAV789)
		xbmc.log(url)
		is_folder = True
		listing.append((url, list_item, is_folder))


	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.endOfDirectory(__handle__)

def list_categories_javstreams():
	#TODO
	list_sites()

def list_categories_youjav():
	#TODO
	list_sites()

def list_categories_javsex():
	#TODO
	list_sites()


def list_categories(site):
	if site == _BEJAV:
		list_categories_bejav()
	elif site == _VJAV:
		list_categories_vjav()
	elif site == _JAVHIHI:
		list_categories_javhihi()
	elif site == _JAV789:
		list_categories_jav789()
	elif site == _JAVSTREAMS:
		list_categories_javstreams()
	elif site == _YOUJAV:
		list_categories_youjav()
	elif site == _JAVSEX:
		list_categories_javsex()
	else:
		list_site(site)

#########################################
#				MODELS					#
#########################################

def list_models_vjav(page):
	#TODO
	list_sites()

def list_models_javhihi(page):
	#TODO
	list_sites()

def list_models_jav789(page):
	#TODO
	list_sites()


def list_models(page, site):

	if site == _VJAV:
		list_models_vjav(page)
	elif site == _JAVHIHI:
		list_models_javhihi(page)
	elif site == _JAV789:
		list_models_jav789(page)
	else:
		list_site(site)

#########################################
#				ROUTER					#
#########################################

def router(paramstring):
	"""
	Router function that calls other functions depending on the provided paramstring
	:param paramstring:
	:return:
	"""
	# Parse a URL-encoded paramstring to the dictionary of {<parameter>: <value>} elements
	params = dict(parse_qsl(paramstring[1:]))

	# Check the parameters passed to the plugin
	if params:
		if params['action'] == 'listsite':
			list_site(params['site'])
		elif params['action'] == 'play':
			play_video(params['link'], params['site'])
		elif params['action'] == 'search':
			search(params['site'])
		elif params['action'] == 'listmodels':
			list_models(params['link'], params['page'])
		elif params['action'] == 'listcategories':
			list_categories(params['site'])
		elif params['action'] == 'listvideos':
			site = params['site']
			if site == _JAVHIHI or site == _JAV789:
				list_videos(params['link'], site, params['page'])
			else:
				list_videos(params['link'], site)
	else:
		list_sites()

if __name__ == '__main__':
	# Call the router function and pass the plugin call parameters to it.
	router(sys.argv[2])
