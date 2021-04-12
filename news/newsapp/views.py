import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsStories,Authors
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST","GET"])
@csrf_exempt
def Login(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    try:
        user = Authors.objects.get(username = uname, password = pwd)
    except:
        return HttpResponse ('Account not correct :(',status=401, content_type='text/plain')
    if pwd == user.password:
        rep = HttpResponse ('Successfully logged in :)',status=200, content_type='text/plain')
        rep.set_cookie('login',True)
        rep.set_cookie('uname',uname)
        return rep
    else:
        return HttpResponse ('Cannot log in :(', status=405, content_type='text/plain')

@csrf_exempt
@require_http_methods(["POST"])
def Logout(request):
    if not request.COOKIES.get('login'):
        return HttpResponse ("ERROR! You're not logged in :(",status=200, content_type='text/plain')
    else:
        rep = HttpResponse ("Successfully logged out :)",status=200, content_type='text/plain')
        rep.delete_cookie('login')
        rep.delete_cookie('uname')
        return rep

@csrf_exempt
@require_http_methods(["POST"])
def PostStory(request):
    if not request.COOKIES.get('login'):
        return HttpResponse ("ERROR! You're not logged in :(",status=200, content_type='text/plain')
    if request.method != 'POST':
        return HttpResponse (status=405, content_type='text/plain')
    authname = Authors.objects.get(username=request.COOKIES.get('uname'))
    story = json.loads(request.body)
    if(request.method == 'POST' and story['category'] in ['tech','pol','art','trivia'] and story['region'] in ['uk','w','eu']):
        story = NewsStories(headline=story['headline'], category=story['category'], author=authname,
                            details=story['details'],   region=story['region'])
        story.save()
        return HttpResponse ("POST successful :)",status=201, content_type='text/plain')
    else:
        return HttpResponse ("Invalid region or category :(",status=503, content_type='text/plain')

@csrf_exempt
@require_http_methods(["POST"])
def GetStory(request):
    story = json.loads(request.body) # a piece of story
    stories = NewsStories.objects.all() # all stories
    listOfStories = []
    if not request.COOKIES.get('login'):
        return HttpResponse ("ERROR! You're not logged in :(",status=200, content_type='text/plain')
    if request.method != 'POST':
        return HttpResponse (status=405, content_type='text/plain')
    # converting to right format
    if stories['story_cat'] != '*':
        stories = stories.filter(category=story.get("story_cat"))
    if stories['story_region'] != '*':
        stories = stories.filter(category=story.get("story_region"))
    if stories['story_date'] != '*':
        construct_date = datetime.datetime.strptime(story.get('story_date'), "%d/%m/%Y").strftime("%Y-%m-%d")
        stories = stories.filter(date=construct_date)
    #print(stories)
    for story in stories:
        story_json_info = {'key' : str(story.key),'headline' : story.headline,'story_cat' : story.category,'story_region' : story.region,'author' : story.author.username,'story_date' : str(story.date),'story_details' : story.detail}
        listOfStories.append(story_json_info)
    print(listOfStories)
    if len(listOfStories) == 0:
        return HttpResponse("No such story :(",content_type="text/plain",status=404)
    rep = json.dumps({'stories':listOfStories})
    return HttpResponse(content=rep,content_type="application/json",status=200)

@csrf_exempt
@require_http_methods(["POST"])
def DeleteStory(request):
    json_data = json.loads(request.body)
    have_story = NewsStories.objects.filter(pk=json_data.get('story_key')).exists()
    if not have_story:
        return HttpResponse ("Story not exist :(",status=503,content_type='text/plain')
    if not request.COOKIES.get('login'):
        return HttpResponse ("ERROR! You're not logged in :(",status=200, content_type='text/plain')
    elif (request.method == 'POST' and request.COOKIES.get('login') and have_story == True):
        NewsStories.objects.filter(pk=json_data.get('story_key')).delete()
        return HttpResponse ("Story deleted :)",status=201, content_type='text/plain')
    else:
        return HttpResponse (status=405, content_type='text/plain')
