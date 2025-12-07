from django.contrib import admin
from .models import Board, Quote


class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "date", "pin")
    readonly_fields = ("code",)


admin.site.register(Board, BoardAdmin)
admin.site.register(Quote)
