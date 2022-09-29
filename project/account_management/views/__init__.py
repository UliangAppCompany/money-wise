from ninja import NinjaAPI


api = NinjaAPI()


class SupercategoryUnavailableError(Exception):
    pass


class DuplicateValueError(Exception):
    pass


@api.exception_handler(SupercategoryUnavailableError)
def parent_category_unavailable(request, exc):
    return api.create_response(
        request,
        {
            "message": "Parent category not found.",
        },
        status=400,
    )


@api.exception_handler(DuplicateValueError)
def duplicate_category_detected(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=403)
