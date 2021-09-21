from django.shortcuts import render

messages = {
    "404": {
        "code": 404,
        "status": "Page not found",
        "message": "Oops! The page you are looking for does not exist. It might have been moved or deleted."
    },
    "403": {
        "code": 403,
        "status": "Forbidden",
        "message": '"Tresspassers will be prosecuted." ~ Developers'
    },
    "500": {
        "code": 500,
        "status": "Server Error",
        "message": ""
    },
}

def errorPage(request, args=messages["404"], **kwargs):
    return render(request, 'home/errorpage.html', args)