from django.shortcuts import render,redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    # for posting data in database
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,TITLE=request.POST['TITLE'],DESCRIPTION=request.POST['DESCRIPTION'])
            notes.save()
        messages.success(request,f"Notes saved by  {request.user.username}  successfully")
    else:
            form=NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes,'form': form}
    return render(request, 'dashboard/notes.html',context)

def delete_notes(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

def delete_notesall(request):
    Notes.objects.all().delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model=Notes

def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homeworks=Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],due=request.POST['due'],is_finished=finished)
            homeworks.save()
            messages.success(request,f"Homworks addedd from {request.user.username}  successfully")

    else:            
        form=HomeworkForm()

    homework = Homework.objects.filter(user=request.user)
    if(len(homework) == 0):
        homework_done = True
    else:
        homework_done =False
    context = {'homeworks': homework,'homework_done':homework_done,'form':form}
    return render(request, 'dashboard/homework.html',context)

def delete_homeworks(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished= False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")

def youtube(request):
    if request.method == 'POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input': text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnails':i['thumbnails'][0]['url'],
                'channel':i['channel'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc =''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc +=j['text']

            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results': result_list
                }

# from youtubesearchpython import VideosSearch

# videosSearch = VideosSearch('NoCopyrightSounds', limit = 2)

# print(videosSearch.result())
# Result
# {
#     "result": [
#         {
#             "type": "video",
#             "id": "K4DyBUG242c",
#             "title": "Cartoon - On & On (feat. Daniel Levi) [NCS Release]",
#             "publishedTime": "5 years ago",
#             "duration": "3:28",
#             "viewCount": {
#                 "text": "389,673,774 views",
#                 "short": "389M views"
#             },
#             "thumbnails": [
#                 {
#                     "url": "https://i.ytimg.com/vi/K4DyBUG242c/hqdefault.jpg?sqp=-oaymwEjCOADEI4CSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLBkTusCwcZQlmVAaRQ5rH-mvBuA1g",
#                     "width": 480,
#                     "height": 270
#                 }
#             ],
#             "descriptionSnippet": [
#                 {
#                     "text": "NCS: Music Without Limitations NCS Spotify: http://spoti.fi/NCS Free Download / Stream: http://ncs.io/onandon \u25bd Connect with\u00a0..."
#                 }
#             ],
#             "channel": {
#                 "name": "NoCopyrightSounds",
#                 "id": "UC_aEa8K-EOJ3D6gOs7HcyNg",
#                 "thumbnails": [
#                     {
#                         "url": "https://yt3.ggpht.com/a-/AOh14GhS0G5FwV8rMhVCUWSDp36vWEvnNs5Vl97Zww=s68-c-k-c0x00ffffff-no-rj-mo",
#                         "width": 68,
#                         "height": 68
#                     }
#                 ],
            
    else:
        form =DashboardForm
    context = {'form':form}
    return render(request, 'dashboard/youtube.html',context)

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todo=Todo(user=request.user,title=request.POST['title'],is_finished=finished)
            todo.save()
            messages.success(request,f"Todo addedd from {request.user.username}  successfully")
    else:
        form =TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if(len(todo) == 0):
        todo_done=True
    else:
        todo_done =False
    context = {
        'form':form,
        'todos':todo,
        'todo_done':todo_done
    }
    return render(request, 'dashboard/todo.html',context)


def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")  

def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished= False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")

def books(request):
    if request.method == 'POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url ="https://www.googleapis.com/books/v1/volumns?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict ={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pagecount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {'form':form,'results':result_list}
            return render(request, 'dashboard/books.html',context)
    else:
        form =DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/books.html',context)


def wiki(request):
    if request.method == 'POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        search= wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary,   
            
        }
        return render(request, 'dashboard/wiki.html',context)
    else:
        form =DashboardForm()
        context = {'form':form}
    return render(request, 'dashboard/wiki.html',context)


def conversion(request):
    if request.method == 'POST':
        form=ConversionForm(request.POST)
        if request.POST['measurement']=='length':
            measurement_form=ConversionLengthForm()
            context = {
            'm_form':measurement_form,
            'form':form,
            'input':True,
            }
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input=request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first=='yard' and second == 'foot':
                        answer=f'{input} yard = {int(input)*3} foot'
                    if first=='foot' and second == 'yard':
                        answer=f'{input} foot = {int(input)/3} yard'
                context = {
                    'm_form':measurement_form,
                    'form':form,
                    'input':True,
                    'answer':answer
                }
        
        if request.POST['measurement']=='mass':
            measurement_form= ConversionMassForm()
            context = {
            'm_form':measurement_form,
            'form':form,
            'input':True,
            }
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input=request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first=='pound' and second == 'kilogram':
                        answer=f'{input} pound = {int(input)*0.453592} kilogram'
                    if first=='kilogram' and second == 'pound':
                        answer=f'{input} kilogram = {int(input)/0.453592} kilogram'
                context = {
                    'm_form':measurement_form,
                    'form':form,
                    'input':True,
                    'answer':answer
                } 
        return render(request, 'dashboard/conversion.html',context)      
    else:
        form=ConversionForm()
        context = {
            'form':form,
            'input':False  
        }
       
    return render(request, 'dashboard/conversion.html',context)