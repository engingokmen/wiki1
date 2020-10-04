from . import util
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from markdown2 import Markdown
markdowner = Markdown()


def index(request):
    # if a query is submitted direct to page
    q = request.GET.get('q')
    if q is not None:
        return direct_query(q)
    # render all entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'title margin-bottom'}), label="Title")
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'margin-bottom'}), label="Description")


class EditPageForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'margin-bottom'}), label="Description")


def create_new_page(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["description"]
            # Add new entry
            if(util.get_entry(title) == None):
                util.save_entry(title, content)
                # Redirect user to the entry detail which is recently added
                return redirect("entry_detail", title)
            else:
                return render(request, "encyclopedia/error.html", {"error": "This entry is already exist."})
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create-new-page.html", {
                "form": form
            })
    return render(request, "encyclopedia/create-new-page.html", {
        "form": NewPageForm()
    })


def edit_page(request, title):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = EditPageForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            content = form.cleaned_data["description"]
            # Add the new task to our list of tasks
            print(f'edit-page title: {title}')
            if(util.get_entry(title) != None):
                util.save_entry(title, content)
                # Redirect user to list of tasks
                return redirect("entry_detail", title)
            else:
                return render(request, "encyclopedia/error.html", {"error": "Check entry and try again"})
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit-page.html", {
                "form": form
            })
    return render(request, "encyclopedia/edit-page.html", {
        'title': title,
        "form": EditPageForm(initial={'description': util.get_entry(title)})
    })


def random_page(request):
    list_entries = util.list_entries()
    random_number = random.randint(0, len(list_entries)-1)
    return redirect('entry_detail', list_entries[random_number])


def entry_detail(request, title):
    # if a query is submitted direct to page
    q = request.GET.get('q')
    if q is not None:
        return direct_query(q)
    # make Entry detail page:
    if util.get_entry(title) is None:
        context = {
            "error": "We could not find the entry that you are looking for"
        }
        return render(request, "encyclopedia/error.html", context)
    context = {
        "title": title,
        "entry": markdowner.convert(util.get_entry(title))
    }
    return render(request, "encyclopedia/entry-detail.html", context)


def search_result(request, query):
    # if a query is submitted direct to page
    q = request.GET.get('q')
    if q is not None:
        return direct_query(q)
    # make Search result page:
    length_query = len(query)
    result_list = []
    for entry in util.list_entries():
        if entry[:length_query] == query:
            result_list.append(entry)
    context = {
        "search_results": result_list
    }
    return render(request, "encyclopedia/search-result.html", context)


def direct_query(q):
    # if the query is matched with one of entries, redirect user to that entry
    if util.return_entry_in_entries(q) is not None:
        return redirect('entry_detail', q)
    # otherwise redirect user to the list of entries
    else:
        return redirect('search_result', q)
