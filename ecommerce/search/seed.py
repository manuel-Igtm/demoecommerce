from .models import SearchHistory

def run():
    print("Seeding search history...")

    SearchHistory.objects.all().delete()

    searches = [
        SearchHistory.objects.create(user_id=1, query="laptop"),
        SearchHistory.objects.create(user_id=2, query="smartphone"),
        SearchHistory.objects.create(user_id=1, query="wireless headphones"),
    ]

    print(f"Seeded {len(searches)} search entries.")

if __name__ == "__main__":
    run()

