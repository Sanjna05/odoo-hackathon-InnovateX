import datetime

# ------------------ Data Storage ------------------
users = []          # Store all users
tickets = []        # Store all tickets
categories = ["General", "Technical", "Billing"]
current_user = None # Store logged-in user

# ------------------ Classes -----------------------
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # admin / agent / user

class Ticket:
    def __init__(self, ticket_id, user, subject, description, category):
        self.ticket_id = ticket_id
        self.user = user
        self.subject = subject
        self.description = description
        self.category = category
        self.status = "Open"  # Open → In Progress → Resolved → Closed
        self.created_at = datetime.datetime.now()
        self.replies = []
        self.upvotes = 0
        self.downvotes = 0
    
    def add_reply(self, reply):
        self.replies.append(reply)

# ------------------ Functions -----------------------

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/agent/user): ").lower()
    users.append(User(username, password, role))
    print(" User registered successfully!\n")

def login():
    global current_user
    username = input("Username: ")
    password = input("Password: ")
    for u in users:
        if u.username == username and u.password == password:
            current_user = u
            print(f" Logged in as {u.username} ({u.role})\n")
            return True
    print(" Invalid credentials!\n")
    return False

def create_ticket():
    subject = input("Enter ticket subject: ")
    description = input("Enter ticket description: ")
    print("Available categories:", categories)
    category = input("Choose category: ")
    ticket_id = len(tickets) + 1
    ticket = Ticket(ticket_id, current_user.username, subject, description, category)
    tickets.append(ticket)
    print(f" Ticket #{ticket_id} created!\n")

def view_my_tickets():
    found = False
    for t in tickets:
        if t.user == current_user.username:
            found = True
            print(f"[#{t.ticket_id}] {t.subject} - {t.status} ({t.category}) "
                  f"Replies: {len(t.replies)} {t.upvotes} {t.downvotes}")
    if not found:
        print("No tickets found!\n")

def search_tickets():
    keyword = input("Enter keyword/category/status: ")
    found = False
    for t in tickets:
        if (keyword.lower() in t.subject.lower() or 
            keyword.lower() in t.category.lower() or 
            keyword.lower() in t.status.lower()):
            found = True
            print(f"[#{t.ticket_id}] {t.subject} - {t.status} ({t.category}) by {t.user}")
    if not found:
        print("No tickets found!\n")

def upvote_ticket():
    ticket_id = int(input("Enter ticket ID to upvote: "))
    for t in tickets:
        if t.ticket_id == ticket_id:
            t.upvotes += 1
            print(" Ticket upvoted!\n")
            return
    print(" Ticket not found!\n")

def downvote_ticket():
    ticket_id = int(input("Enter ticket ID to downvote: "))
    for t in tickets:
        if t.ticket_id == ticket_id:
            t.downvotes += 1
            print(" Ticket downvoted!\n")
            return
    print(" Ticket not found!\n")

def agent_dashboard():
    for t in tickets:
        print(f"[#{t.ticket_id}] {t.subject} - {t.status} ({t.category}) by {t.user}")
    ticket_id = int(input("Enter ticket ID to update status/reply (0 to exit): "))
    if ticket_id == 0: return
    for t in tickets:
        if t.ticket_id == ticket_id:
            new_status = input("Enter new status (Open/In Progress/Resolved/Closed): ")
            t.status = new_status
            reply = input("Enter reply: ")
            t.add_reply(f"{current_user.username}: {reply}")
            print("✅ Ticket updated!\n")
            return
    print(" Ticket not found!\n")

def admin_dashboard():
    print("1. Create category\n2. View users\n")
    choice = input("Choose: ")
    if choice == "1":
        new_cat = input("Enter new category: ")
        categories.append(new_cat)
        print("✅ Category added!\n")
    elif choice == "2":
        for u in users:
            print(f"{u.username} - {u.role}")
        print()

# ------------------ Main Menu -----------------------

def main_menu():
    while True:
        print("\n----- QuickDesk -----")
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            register()
        elif choice == "2":
            if login():
                dashboard()
        elif choice == "3":
            print("Exiting QuickDesk... Goodbye!")
            break

def dashboard():
    while True:
        if current_user.role == "user":
            print("\n----- User Menu -----")
            print("1. Create Ticket\n2. View My Tickets\n3. Search Tickets")
            print("4. Upvote Ticket\n5. Downvote Ticket\n6. Logout")
            choice = input("Choose: ")
            if choice == "1": create_ticket()
            elif choice == "2": view_my_tickets()
            elif choice == "3": search_tickets()
            elif choice == "4": upvote_ticket()
            elif choice == "5": downvote_ticket()
            elif choice == "6": break

        elif current_user.role == "agent":
            print("\n----- Agent Menu -----")
            print("1. View/Update Tickets\n2. Logout")
            choice = input("Choose: ")
            if choice == "1": agent_dashboard()
            elif choice == "2": break

        elif current_user.role == "admin":
            print("\n----- Admin Menu -----")
            print("1. Admin Dashboard\n2. Logout")
            choice = input("Choose: ")
            if choice == "1": admin_dashboard()
            elif choice == "2": break

# Pre-register an admin for testing
users.append(User("admin", "admin", "admin"))

main_menu()
