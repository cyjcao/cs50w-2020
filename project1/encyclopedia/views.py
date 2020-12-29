from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import util
import markdown2


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
    


