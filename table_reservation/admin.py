from django.contrib import admin

# Register your models here.
from table_reservation.models import Table, Time_Table, Table_Reserve

class Time_tableInline(admin.TabularInline):
    model = Time_Table
    fk_name = 'parent_table'
    extra = 1
    show_change_link = True


class TableAdmin(admin.ModelAdmin):
    list_display = ['title', 'seat', 'total']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [Time_tableInline, ]


class Time_TableAdmin(admin.ModelAdmin):
    list_display = ['title', 'hour_selection']
    prepopulated_fields = {'slug': ('title',)}

class Table_ReserveAdmin(admin.ModelAdmin):
    list_display = ['user', 'table', 'time_table', 'on_date', 'time_from', 'time_to']
admin.site.register(Table, TableAdmin)
admin.site.register(Time_Table, Time_TableAdmin)
admin.site.register(Table_Reserve, Table_ReserveAdmin)


