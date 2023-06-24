from django.core.management.base import BaseCommand
from apps.garage.models import Doc


class Command(BaseCommand):
    help = "Convert lbs to kgs"

    def add_arguments(self, parser):
        parser.add_argument("userid", type=int, help="Which user to update")

    def handle(self, *args, **kwargs):
        docs = Doc.objects.filter(user_id=kwargs["userid"], doc_type="hp")
        if docs:
            for doc in docs:
                if doc.data["type"] == "weight":
                    print("Org:", doc.data)
                    data = doc.data
                    data["weight"] = round(data["weight"] * 0.45359237)
                    doc.data = data
                    doc.save()
                    print("Converted:", doc.data)
        else:
            print("Try another ID, no hp docs found")


