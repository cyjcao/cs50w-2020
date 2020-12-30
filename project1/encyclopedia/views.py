from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from django import forms

from . import util

from random import randint
import markdown2



class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

    # this function will be used for validation
    def clean(self):
        super(NewPageForm, self).clean()

        title = self.cleaned_data.get('title')

        existing_entries = util.list_entries()
        
        # title should not already exist
        if title.lower() in [entry.lower() for entry in existing_entries]:
            self._errors['title'] = self.error_class([
                'Entry with same title already exists'
            ])
        
        # return any errors if found
        return self.cleaned_data

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    contents = util.get_entry(title)
    # load page for corresponding entry if file exists, if not raise a 404 not found error
    if contents:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "contents": markdown2.markdown(contents)
        })
    else:
        raise Http404

@require_http_methods(["POST"])
def search(request):
    """
    Redirects user to entry page matching the user query. If no exact match, display a page with search results of entry titles that has query as substring
    """
    query = request.POST['q']
    contents = util.get_entry(query)
    # if query matches name of an entry, redirect user to the entry's page
    # if not, user is taken to search results page which contains list of entry names that has the query as a substring
    if contents:
        return HttpResponseRedirect(reverse('entry', args=[query]))
    else:
        all_entries = util.list_entries()
        search_results = []
        for entry in all_entries:
            if query.lower() in entry.lower():
                search_results.append(entry)
        
        return render(request, "encyclopedia/search.html", {
            "title": "Search Results",
            "results": search_results
        })

def new(request):
    """
    Allows user to create a new page entry
    """
    if request.method == "POST":
        form = NewPageForm(request.POST)

        # Check if form is valid (if entry with title doesn't already exist)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            util.save_entry(title, content)

            # redirect user to new page
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            # if form is invalid, re-render page with existing information and error message
            return render(request, "encyclopedia/new.html", {
                "title": "Create New Page",
                "section_title": "Create New Page",
                "url": request.path,
                "form": form
            })

    return render(request, "encyclopedia/new.html", {
        "title": "Create New Page",
        "section_title": "Create New Page",
        "url": request.path,
        "form": NewPageForm()
    })

def edit(request, title):
    """
    Allows user to edit an existing entry page
    """
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse('entry', args=[title]))
    else:
        contents = util.get_entry(title)
        form = NewPageForm(initial={'title': title, 'content': contents})
        form.fields['title'].disabled = True
        return render(request, 'encyclopedia/new.html', {
            "title": "Edit Page",
            "section_title": "Edit Page",
            "url": request.path,
            "form": form
        })

def random(request):
    """
    Redirects user to a random entry page
    """
    entries = util.list_entries()
    rand_entry = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect(reverse('entry', args=[rand_entry]))

