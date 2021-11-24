from fishapp.models import Category
# from fishapp.utils import


def portal_processor(request):
    return {'PORTAL_URL': request.build_absolute_uri('/')[:-1]}

# request.build_absolute_uri(location) - повертає абсолютний URL до location
# [:-1] - повертаємо значення без '/', щоб його не дублювати


def get_categories(request):
    return {'categories': Category.annotate_objects.get_categories_for_left_sidebar()}
