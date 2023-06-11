from django.shortcuts import render

# Create your views here.
from table_reservation.models import Table, Time_Table, Table_Reserve


def table_book(request):
    current_user = request.user
    tables = Table.objects.all()
    time_tables = Time_Table.objects.all()

    context = {'tables': tables, 'time_tables': time_tables, }
    return render(request, 'book_table.html', context)


