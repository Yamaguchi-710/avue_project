from django.apps import AppConfig
# import function


class AppConfig(AppConfig):
    # 追加
    # list_route = function.make()
    # function.print_prj(list_route)
    #
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
