from apps.users.models import User

u = User.objects.filter(email="admin@esc-shipping.com").first()
if u:
    print(f"Email: {u.email}")
    print(f"Staff: {u.is_staff}")
    print(f"Superuser: {u.is_superuser}")
    print(f"Active: {u.is_active}")
    print(f"Password check: {u.check_password('admin123')}")
else:
    print("Admin user not found!")
