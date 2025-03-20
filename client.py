import xmlrpc.client

# Connect to server
server = xmlrpc.client.ServerProxy("http://localhost:9000")

#Very simple menu structure with very basic error handling
def main():
    while True:
        print("1. Add note")
        print("2. Get notes")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            topic = input("Enter topic: ")
            note = input("Enter note: ")
            text = input("Enter text: ")

            print(server.add_note(topic, note, text))

        elif choice == "2":
            topic = input("Enter topic: ")
            notes = server.get_notes(topic)
            for note in notes:
                print(note)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
