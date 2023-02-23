import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import url

from chat.forms import ContactForm
from chat.models import Message


def home(req):
    return render(req, "basemain.html")


def about(req):
    return render(req, "about.html")


def contact(req):
    if req.method == "POST":
        form = ContactForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("thanks")
    else:
        form = ContactForm()
    return render(req, "contact.html", context={'form': form})


def register(req):
    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect(req.GET.get("next") or url("home"))
    else:
        form = UserCreationForm()
    return render(req, "registration/register.html", context={"form": form})


# def profile(req, id):
#     prof = get_object_or_404(Profile, id=id)
#     return render(req, "profile.html", context={"form": prof})


def thanks(req):
    return render(req, "thanks.html")


# @login_required
# def profile_edit(req):
#     if req.method == "POST":
#         form = ProfileForm(req.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("contact thanks")
#     else:
#         form = ProfileForm()
#     return render(req, "profile_edit.html", context={"form": form})


@login_required
def chat(req):
    return render(req, "chatindex.html")


@login_required
def api_log(req):
    log = Message.objects.filter(index=0, deleted=False)[:100]
    for item_no in range(log):
        if log[item_no].edited:
            log[item_no] = Message.objects.filter(msg_id=log[item_no].msg_id).order_by("-index")[0]
    return render(req, "api_log.html", context={"messages": log})


@login_required
def api_new(req):
    validation_errors = []

    if not req.POST.get("query"):
        validation_errors += ["No json processed"]

    jso = json.loads(req.POST.get("query"))

    if not type(jso["body"]) == "String":
        validation_errors += ["Incorrect message type"]

    if not type(jso["profile_id"]) == "Integer":
        validation_errors += ["Incorrect profile id format"]

    if validation_errors:
        return render(req, "errors.html", context={"validation_errors": validation_errors})

    msg_id = Message.objects.all().order_by("-msg_id")[0].msg_id + 1

    msg = Message(msg_id=msg_id, body=jso["body"], profile_id=jso["profile_id"])
    msg.save()

    return render(req, "jsonsuccess.html")


@login_required
def api_edit(req):
    validation_errors = []

    if not req.POST.get("query"):
        validation_errors += ["No json processed"]
        return render(req, "errors.html", context={"validation_errors": validation_errors})

    jso = json.loads(req.POST.get("query"))
    old_msg = Message.objects.filter(msg_id=req.POST.get("query")).order_by("-index")[0]

    if not old_msg.exists():
        validation_errors += ["No message to update with that id"]
        return render(req, "errors.html", context={"validation_errors": validation_errors})

    if jso["delete"] == True:
        old_msg.deleted = True
        old_msg.save()
        return render(req, "jsonsuccess.html")

    if not jso["body"]:
        validation_errors += ["No new message body"]
        return render(req, "errors.html", context={"validation_errors": validation_errors})

    msg = Message(index=old_msg.index+1, msg_id=old_msg.msg_id, body=jso["body"])
    msg.save()

    return render(req, "jsonsuccess.html")
