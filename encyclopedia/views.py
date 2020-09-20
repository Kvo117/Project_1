from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from random import choice

markdowner = Markdown()

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title", widget=forms.TextInput)
    body = forms.CharField(label="New Entry", widget=forms.Textarea)

class EditEntryForm(forms.Form):
    body = forms.CharField(widget= forms.Textarea, label="Content")


#complete
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#complete
def entry(request, title):
    entries = util.get_entry(title) #the call to the function that gets the entry
    if entries == None: #something wrong with this logic
        return render(request, "encyclopedia/error.html", {
            "error": "The page could not be found V2."})
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(entries),
            "nameOfEntry": title
        })


#complete
def search(request):
    title = request.GET['q'] #django dictionary object containing all GET request parameters; returns the value for the q, in this case its the page of the title, q
    entries = util.get_entry(title)
    listOfEntries = util.list_entries()
    first = []
    if entries != None:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(entries),
            "nameOfEntry": title
        })
    else:
        for entry in listOfEntries:
            if title in entry:
                first.append(entry)
        if len(first) > 0: #if there is at least one entry within the list/array
            return render(request, "encyclopedia/results.html", {
                "first": first
            })
        else:
            return render(request, "encyclopedia/error.html", {
            "error": "The page could not be found."})


#need the button to redirect to home/new 
#issue with clicking "create a new page" in an entry form
def add(request):
    if request.method == "POST": #if sending data to the server by clicking save
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", { #this render is correct
                "error":'A file with this title already exists.'
                })
            else:
                util.save_entry(title, body)
                return redirect("/wiki/" + title) #the redirect works; saves then redirects to the new page
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form":form
            })
    return render(request, "encyclopedia/newPage.html", {
            "form": NewEntryForm() #this render is correct
                })


#edit functionality is complete
def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "error": "this is the edit error"
            })
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    elif request.method == "POST":
        content = request.POST.get("edit_content")
        util.save_entry(title, content)
        return redirect("entry", title)


#def random(request):
#    entries = util.list_entries()

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))