from django.http import JsonResponse


def method(allowed=None, denied=None):
    def __params(fnc):
        def __method(request):
            if denied is not None:
                if request.method in denied:
                    return JsonResponse({"ok": False, "message": "Wrong connection"})
            if allowed is not None:
                if request.method not in allowed:
                    return JsonResponse({"ok": False, "message": "Wrong connection"})
            return fnc(request)
        return __method
    return __params

