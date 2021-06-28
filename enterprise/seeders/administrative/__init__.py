import csv
import os

from enterprise.structures.administrative.models import (
    Province,
    Regency,
    District,
    Village,
)

CSV_DIRECTORY = "%s/administrative/csv" % os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


def clean_all():
    provinces = Province.objects.all()
    total_provinces = provinces.count()
    provinces.delete()

    print(f"success delete {total_provinces} provinces")


def import_province():
    with open(CSV_DIRECTORY + "/provinces.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            id = row[0]
            name = row[1]

            try:
                Province.objects.get_or_create(id=id, name=name)
                line_count += 1
            except Exception as error:
                print({"name": name, "error": str(error)})

            print(f"Processed {line_count} lines.")


def import_regency():
    with open(CSV_DIRECTORY + "/regencies.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            id = row[0]
            province_id = row[1]
            name = row[2]

            try:
                province = Province.objects.get(id=province_id, name=name)
                Regency.objects.get_or_create(id=id, province=province, name=name)

                line_count += 1
            except Exception as error:
                print({"name": name, "error": str(error)})

            print(f"Processed {line_count} lines.")


def import_district():
    with open(CSV_DIRECTORY + "/districts.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            id = row[0]
            regency_id = row[1]
            name = row[2]

            try:
                regency = Regency.objects.get(id=regency_id, name=name)
                District.objects.get_or_create(id=id, regency=regency, name=name)

                line_count += 1
            except Exception as error:
                print({"name": name, "error": str(error)})

            print(f"Processed {line_count} lines.")


def import_village():
    with open(CSV_DIRECTORY + "/villages.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            id = row[0]
            district_id = row[1]
            name = row[2]

            try:
                district = District.objects.get(id=district_id, name=name)
                Village.objects.get_or_create(id=id, district=district, name=name)

                line_count += 1
            except Exception as error:
                print({"name": name, "error": str(error)})

            print(f"Processed {line_count} lines.")


def import_all(delete_previouse=False):
    if delete_previouse:
        clean_all()
    print("Process Provinces ...")
    import_province()

    print("Process Regencies ...")
    import_regency()

    print("Process Districts ...")
    import_district()

    print("Process Villages ...")
    import_village()

    print("All data processed")
