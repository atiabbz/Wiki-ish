from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import markdown2
import random
from django.core.files.storage import default_storage

from . import util


def index(request):
    return render(request, "encyclopedia/index.html",
                  {"entries": util.list_entries()})



def entry(request, title):
    entryMd = util.get_entry(title)
    # print(entryMd)
    if entryMd is None:
        return render(request, "encyclopedia/nonexistent.html",
                      {"title": title})
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entryMd),
            "title": title
        })

def randomEntry(request):
    entries = util.list_entries()
    randomTitle = entries[random.randint(0, len(entries)-1)]
    return HttpResponseRedirect(reverse("entry", args=(randomTitle,)))

def search(request):
    q = request.GET["q"].lower()
    entries = util.list_entries()

    results = []
    for entry in entries:
        if q == entry.lower():
            return HttpResponseRedirect(reverse("entry", args=(entry, )))
        if q in entry.lower():
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "results": results
    })

def new(request):
    if request.method == "POST":
        entries = util.list_entries()
        title = request.POST["title"]
        if title in entries:
            return render(request, 'encyclopedia/exists.html', {
                'title': title
            })

        content = "# " + title + "\n\n" + request.POST["body"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=(title,)))
    return render(request, "encyclopedia/new.html")


class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = "# " + title + "\n\n" + form.cleaned_data["content"]
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=(title, )))

    content = util.get_entry(title)[2+len(title):].lstrip()
    form = EditForm(initial={"content": content})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
        "form": form,
    })