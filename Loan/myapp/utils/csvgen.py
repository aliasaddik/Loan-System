import csv
from django.http import HttpResponse

def generate_csv_response(queryset, filename, header_row, field_names):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(header_row)

    for obj in queryset:
        writer.writerow([getattr(obj, field_name) for field_name in field_names])

    return response