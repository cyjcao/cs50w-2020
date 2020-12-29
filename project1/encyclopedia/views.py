from django.shortcuts import render
from django.http import Http404

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    contents = util.get_entry(title)
    if contents:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "contents": markdown2.markdown(contents)
        })
    else:
        raise Http404


