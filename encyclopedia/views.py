from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
import markdown
import random
from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries":  util.list_entries()
    })


def entry(request, title):
    # Use util.get_entry to fetch the content
    content = util.get_entry(title)
    
    if content is None:
        # If the content is None, render the error page
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        # Convert Markdown to HTML and render the entry page
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": " Please choose another title.",
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render (request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
def edit_page(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)

         # If entry does not exist, show an error page
        if entry is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The entry does not exist."
            })
        
        # Render the edit page with the existing content in a textarea
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": entry
        })
    else:
        # Handle saving the updated content when the form is submitted
        new_content = request.POST["content"]  # Get the updated content from the form
        util.save_entry(title, new_content)  # Save the updated content

        # Redirect to the entry page with the updated content
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
def random_page(request):
    # Get all the entry titles
    entries = util.list_entries()  # Assuming you have a method that returns a list of all entry titles
    
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
    
    # Choose a random entry
    random_entry = random.choice(entries)
    
    # Redirect to the random entry page
    return redirect('entry', title=random_entry)
      
    