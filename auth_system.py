import uuid
import hashlib
from datetime import datetime, timedelta


class AuthSystem:
    def __init__(self):
        self.users = {}       # store user data
        self.tokens = {}      # store token sessions
        self.groups = {}      # store groups

    # hash password
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # generate token
    def _generate_token(self, username):
        token = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(hours=1)
        self.tokens[token] = {"user": username, "expires_at": expiry}
        return token

    # 1. Register
    def register(self, username, password, email):
        # check if username/email exists
        for u in self.users.values():
            if u["email"] == email:
                return "Email already exists"
        if username in self.users:
            return "Username already exists"

        self.users[username] = {
            "username": username,
            "password": self._hash_password(password),
            "email": email,
            "groups": [],
            "token": None,
            "email_verified": False,
            "created_at": datetime.now(),
            "last_login": None,
            "failed_attempts": 0,
            "locked_until": None
        }
        return "User registered successfully"

    # 2. Login
    def login(self, username, password):
        if username not in self.users:
            return "User not found"
        user = self.users[username]

        # check if account locked
        if user["locked_until"] and datetime.now() < user["locked_until"]:
            return "Account is locked. Try again later."

        if user["password"] == self._hash_password(password):
            token = self._generate_token(username)
            user["token"] = token
            user["last_login"] = datetime.now()
            user["failed_attempts"] = 0  # reset
            return f"Login successful. Token: {token}"
        else:
            user["failed_attempts"] += 1
            if user["failed_attempts"] >= 3:
                user["locked_until"] = datetime.now() + timedelta(minutes=5)
                user["failed_attempts"] = 0
                return "Account locked due to too many failed attempts."
            return "Invalid credentials"

    # 3. Logout
    def logout(self, token):
        if token in self.tokens:
            user = self.tokens[token]["user"]
            self.users[user]["token"] = None
            del self.tokens[token]
            return "Logged out successfully"
        return "Invalid token"

    # 4. Reset Password
    def reset_password(self, username, old_password, new_password):
        if username not in self.users:
            return "User not found"
        user = self.users[username]
        if user["password"] == self._hash_password(old_password):
            user["password"] = self._hash_password(new_password)
            return "Password updated successfully"
        return "Old password does not match"

    # 5. Grouping
    def create_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = []
            return "Group created"
        return "Group already exists"

    def add_user_to_group(self, username, group_name):
        if username not in self.users:
            return "User not found"
        if group_name not in self.groups:
            return "Group not found"
        if username not in self.groups[group_name]:
            self.groups[group_name].append(username)
            self.users[username]["groups"].append(group_name)
            return "User added to group"
        return "User already in group"

    def check_access(self, username, group_name):
        if username in self.users and group_name in self.groups:
            return username in self.groups[group_name]
        return False

    # 6. Email Verification
    def verify_email(self, username):
        if username in self.users:
            self.users[username]["email_verified"] = True
            return "Email verified"
        return "User not found"

    # 7. Get Profile
    def get_profile(self, username):
        if username in self.users:
            user = self.users[username]
            return {
                "username": user["username"],
                "email": user["email"],
                "groups": user["groups"],
                "email_verified": user["email_verified"],
                "created_at": user["created_at"],
                "last_login": user["last_login"]
            }
        return "User not found"
# Menu


def interactive():
    auth = AuthSystem()
    while True:
        print("\n--- Authentication System Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. Reset Password")
        print("5. Create Group")
        print("6. Add User to Group")
        print("7. Check Access")
        print("8. Verify Email")
        print("9. Get Profile")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            u = input("Username: ")
            p = input("Password: ")
            e = input("Email: ")
            print(auth.register(u, p, e))

        elif choice == "2":
            u = input("Username: ")
            p = input("Password: ")
            print(auth.login(u, p))

        elif choice == "3":
            t = input("Token: ")
            print(auth.logout(t))

        elif choice == "4":
            u = input("Username: ")
            old = input("Old Password: ")
            new = input("New Password: ")
            print(auth.reset_password(u, old, new))

        elif choice == "5":
            g = input("Group name: ")
            print(auth.create_group(g))

        elif choice == "6":
            u = input("Username: ")
            g = input("Group name: ")
            print(auth.add_user_to_group(u, g))

        elif choice == "7":
            u = input("Username: ")
            g = input("Group name: ")
            print(auth.check_access(u, g))

        elif choice == "8":
            u = input("Username: ")
            print(auth.verify_email(u))

        elif choice == "9":
            u = input("Username: ")
            print(auth.get_profile(u))

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    interactive()
