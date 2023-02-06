from django.shortcuts import render
from django.http import JsonResponse
from .models import Comment, Issue
from django.utils.datetime_safe import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json


def get_issues(request, *args, **kwargs):
    parameters = {
        "beforeDate": request.GET.get("beforeDate", "9999-12-31"),
        "afterDate": request.GET.get("afterDate", "1970-01-01"),
        "author": request.GET.get("author", ""),
        "tracked": request.GET.get("tracked", ""),
        "status": request.GET.get("status", ""),
        "subject": request.GET.get("subject", ""),
        "summary": request.GET.get("summary", ""),
        "description": request.GET.get("description", ""),
        "slug": request.GET.get("slug", ""),
        "order_by": request.GET.get("order_by", "-date"),
    }

    filter_params = {
        i: j
        for i, j in parameters.items()
        if j not in ["", None] and i not in ["order_by", "beforeDate", "afterDate"]
    }

    # print(ob)
    issues = [
        {
            "summary": x.summary,
            "subject": x.subject,
            "description": x.description,
            "tracked": x.tracked,
            "status": x.status,
            "date": x.date,
            "author": x.author,
            "slug": x.slug,
            "votes": x.votes,
            "tvotes": x.tvotes,
            "tags": x.tags,
            "comments": [
                {
                    "description": y.description,
                    "user": y.user,
                    "username": y.username,
                    "timestamp": y.timestamp,
                    "votes": y.votes,
                    "slug": y.slug,
                    "tags": y.tags,
                } for y in Comment.objects.filter(issue=x) if y is not None
            ]
        }
        for x in Issue.objects.filter(
            **filter_params,
            date__lte=parameters["beforeDate"],
            date__gte=parameters["afterDate"]
        ).order_by(parameters["order_by"])
    ]



    return JsonResponse(issues, safe=False)
