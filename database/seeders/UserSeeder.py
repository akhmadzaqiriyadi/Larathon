class UserSeeder:
    def run(self):
        # contoh seeding, nanti bisa dihubungkan ke model/database
        print("Seeding users...")
        users = [
            {"name": "Admin", "email": "admin@test.com"},
            {"name": "User", "email": "user@test.com"}
        ]
        for u in users:
            print(f"Inserting {u}")
