from django.http.response import JsonResponse
from django.shortcuts import render
import datetime
import time
import json
import random

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .forms import MangeUsersForm
from .models import ResearchesList, Users, Journals

# Create your views here.

FIELDS = ["username", "email", "role", "university", "department", "status"]

ROLES = ["guest", "researcher", "journal"]
STATUS = ["waiting", "approved", "rejected"]

JOURNAL_FIELDS = ["journal_name", "publisher", "main_category",  "quartile_rank", "status" ]


def users_view(request):
    users = Users.objects.all()
    context = {
        "users": users
    }
    return render(request, "users.html", context=context)


def journal_view(request):
    journals = Journals.objects.all()
    context = {
        "journals": journals
    }
    return render(request, "journal.html", context=context)


def reports_view(request):
    return render(request, "report.html")


def reports_results(request):
    name = request.GET.get("name")
    type = request.GET.get("type")
    start_year = request.GET.get("start_year")
    end_year = request.GET.get("end_year")
    result = None
    if type == "research":
        result = ResearchesList.objects.filter(
            auther__iexact=name, publish_date__year__gte=start_year, publish_date__year__lte=end_year)
    if type == "dept":
        result = ResearchesList.objects.filter(
            user__department__exact=name, start_date__year__gte=start_year, finish_date__year__lte=end_year)

    return render(request, "view_report.html", {"researches": result, "type": type, "report_date": datetime.date.today()})


def validate_user(user_data):
    for field in FIELDS:
        f = user_data.get(field, None)
        if f is None or f == "":
            return False, f"{field} can't be empty!"
    # Check for role
    if user_data.get("role").lower() not in ROLES:
        return False, f"Role can only be: {', '.join(ROLES)}"

    # Check status
    if user_data.get("status").lower() not in STATUS:
        return False, f"Status can only be: {', '.join(STATUS)}"

    return True, ''


def validate_journal(journal_data):
    for field in JOURNAL_FIELDS:
        f = journal_data.get(field, None)
        if f is None or f == "":
            print(field, f, journal_data)
            return False
    # try:
    #     journal_data["publish_year"] = int(journal_data["publish_year"])
    # except:
    #     return False
    return True

def validate_journal_status(journal_status):
    if journal_status not in STATUS:
        return False
    else:
        return True


def users_management(request):
    if request.method != "POST":
        return JsonResponse(status=405, data={
            "error": "Only POST allowed!"
        })

    data = json.loads(request.body)

    if data.get("type") == "delete":
        user_id = int(data.get("user_id"))
        Users.objects.filter(id=user_id).delete()
        return JsonResponse({
            "deleted": user_id
        })
    if data.get("type") == "update":
        try:
            user_id = int(data.get("user_id"))
            updated_info = data.get("data")
            valid, msg = validate_user(updated_info)
            if not valid:
                return JsonResponse(status=400, data={
                    "error": msg
                })
            user = Users.objects.filter(id=user_id).update(**updated_info)
            return JsonResponse({
                "updated": user_id
            })
        except Exception as e:
            return JsonResponse(status=500, data={
                "error": e.args
            })
    if data.get("type") == "create":
        valid, msg = validate_user(data.get("data"))
        if not valid:
            return JsonResponse(status=400, data={
                "error": msg
            })
        try:
            user = Users.objects.create(**data.get("data"))
            return JsonResponse({
                "created": user.username
            })
        except Exception as e:
            return JsonResponse(status=400, data={
                "error": str(e.args)
            })

    return JsonResponse(status=400, data={
        "error": "event type unknown"
    })


def journals_management(request):
    if request.method != "POST":
        return JsonResponse(status=405, data={
            "error": "Only POST allowed!"
        })

    data = json.loads(request.body)

    if data.get("type") == "delete":
        journal_name = data.get("journal_name")
        Journals.objects.filter(journal_name=journal_name).delete()
        return JsonResponse({
            "deleted": journal_name
        })
    if data.get("type") == "update":
        try:
            journal_name = data.get("journal_name")
            updated_info = data.get("data")
            valid_status = validate_journal_status(updated_info.get("status"))
            valid = validate_journal(updated_info)

            if not valid:
                return JsonResponse(status=400, data={
                    "error": f"Empty data! {','.join(JOURNAL_FIELDS)} are required."
                })
            elif not valid_status:
                return JsonResponse(status=400, data={
                    "error": f"Invalid Status! Should be one of {','.join(STATUS)}"
                })
            else:
                journal = Journals.objects.filter(
                    journal_name=journal_name).update(**updated_info)
                return JsonResponse({
                    "updated": journal_name
                })
        except Exception as e:
            return JsonResponse(status=500, data={
                "error": e.args
            })
    if data.get("type") == "create":
        save_data = data.get("data")
        valid_status = validate_journal_status(save_data.get("status"))
        valid = validate_journal(save_data)

        if not valid:
            return JsonResponse(status=400, data={
                "error": f"Empty data! {','.join(JOURNAL_FIELDS)} are required."
            })
        elif not valid_status:
            return JsonResponse(status=400, data={
                "error": f"Invalid Status! Should be one of {','.join(STATUS)}"
            })
        else:
            try:
                journal = Journals.objects.create(**save_data)
                return JsonResponse({
                    "created": journal.journal_name
                })
            except Exception as e:
                return JsonResponse(status=400, data={
                    "error": str(e.args)
                })

    return JsonResponse(status=400, data={
        "error": "event type unknown"
    })


def generate_view(request):

    number_of_users = int(request.GET.get("n", 10))
    for i in range(number_of_users):
        user = {
            "fullname": f"Full Name {i+1}",
            "role": f"Role {i+1}",
            "university": f"Uni {i+1}",
            "department": f"Dept {i+1}",
            "mobile_number": f"0101010101",
            "office_number": f"0101010101",
            "email": f"user{i+1}@gmail.com",
            "password": "1234",
            "username": f"user{i+1}"
        }
        Users.objects.create(**user)
        journal = {
            "name": f"Journal {i+1}",
            "publisher": f"Publisher {i+1}",
            "publish_year": random.randint(2000, 2021),
            "category": f"Category {i+1}",
            "rank": f"Rank {i+1}",
        }
        Journals.objects.create(**journal)
    return JsonResponse({
        "created": number_of_users
    })


def random_date(s=952627608, e=int(time.time())):
    d = random.randint(s, e)
    return datetime.date.fromtimestamp(d)


def generate_researches_view(request):
    research = int(request.GET.get("n", 50))
    departments = ["Health Information Management and Technology Department",
                   "Environmental Health Department", "Public Health Department"]
    for i in range(research):
        r = {
            "title": f"Title {i+1}",
            "auther": f"Author {i+1}",
            "auther1": "author a",
            "auther2": "author b",
            "auther3": "author c",
            "auther4": "author d",
            "auther5": "author e",
            "auther6": "author f",
            "abstract": f"Research abstract {i+1}",
            "publish_date": random_date(),
            "start_date": random_date(),
            "finish_date": random_date(),
            "research_url": "research.com",
            "journal_name": f"Journal {i+1}",
            "research_category": f"Category {i+1}",
            # "department": random.choice(departments),
            "user_id":request.user.id
        }
        ResearchesList.objects.create(**r)
    return JsonResponse({
        "created": research
    })


# Users request and view requests pages
class UsersView(ListView):
    model = Users
    context = {}
    template_name = 'DisplayUsers.html'
    queryset = Users.objects.filter(status='Approved')
    # return render(request, "view_report.html",context)



class UsersDetailsView(DetailView):
    model = Users
    template_name = 'UsersView.html'
    queryset = Users.objects.all()


class UpdateUpdateView(UpdateView):
    model = Users
    form_class = MangeUsersForm
    template_name = 'UsersUpdate.html'
    success_url = reverse_lazy('users')



class UpdateDeleteView(DeleteView):
    model = Users
    form_class = MangeUsersForm
    template_name = 'DeleteUsers.html'
    success_url = reverse_lazy('users')


