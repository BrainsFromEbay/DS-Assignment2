from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import datetime

DB_FILENAME = "mock_database.xml"

#Function to add notes to the databse
def add_note(topic, note, text):
    try:
        timestamp = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

        tree = ET.parse(DB_FILENAME)
        root = tree.getroot()

        #Check if a note with the same topic already exists
        topic_element = ""
        for element in root.findall("topic"):
            if element.get("name") == topic:
                topic_element = element
                break

        #If the topic does not exist, create a new one
        if topic_element == "":
            topic_element = ET.SubElement(root, "topic")
            topic_element.set("name", topic)

        #Add the note to the topic
        note_element = ET.SubElement(topic_element, "note")
        note_element.set("name", note)

        text_element = ET.SubElement(note_element, "text")
        text_element.text = text

        timestamp_element = ET.SubElement(note_element, "timestamp")
        timestamp_element.text = timestamp

        #Write the changes to the database AND also make sure the XML is properly formatted/prettified (not necessary)
        ET.indent(tree, space="    ")
        with open(DB_FILENAME, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)

        return "Note added successfully."

    except Exception as e:
        return "Error adding note: " + str(e)

def get_notes(topic):
    try:
        tree = ET.parse(DB_FILENAME)
        root = tree.getroot()

        #We go through the database and try to find the topic. We then build "notes" with the notes found.
        for topic_element in root.findall("topic"):
            if topic_element.get("name") == topic:
                notes = []
                for note_element in topic_element.findall("note"):
                    note = note_element.get("name")
                    text = note_element.find("text").text
                    timestamp = note_element.find("timestamp").text
                    notes.append((note, text, timestamp))

                return notes
        return []
    except Exception as e:
        return "Error getting notes: " + str(e)

#Define the server 
def run_server():
    server = SimpleXMLRPCServer(("localhost", 9000))
    print("Listening on port 9000...")

    #Register the functions that the client can access
    server.register_function(add_note, "add_note")

    server.register_function(get_notes, "get_notes")

    server.serve_forever()

#Run the server
if __name__ == "__main__":
    run_server()