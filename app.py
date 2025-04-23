from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# In-memory storage for journal entries
journal_entries = []
# Variable to assign unique IDs to each journal entry
next_id = 1

# Route for the homepage, renders the main index page
@app.route('/')
def index():
    """
    Handles GET request for the root URL ('/').
    Renders the index.html page, which serves as the homepage where users can interact with the journal.
    """
    return render_template('index.html')

# Route to create a new journal entry
@app.route('/journal', methods=['POST'])
def create_entry():
    """
    Handles POST requests to create a new journal entry.
    - Extracts data (date and content) from the JSON body of the request.
    - Assigns a unique ID to the new entry using the `next_id` variable.
    - Appends the new entry to the `journal_entries` list.
    - Increments the `next_id` variable to ensure future entries get unique IDs.
    - Returns the created entry as a JSON response with HTTP status code 201 (Created).
    """
    global next_id
    data = request.get_json()  # Get the data sent in the request body as JSON
    new_entry = {
        'id': next_id,           # Assign the current value of next_id as the entry's ID
        'date': data['date'],    # Extract date from the request data
        'content': data['content']  # Extract content from the request data
    }
    journal_entries.append(new_entry)  # Add the new entry to the list of journal entries
    next_id += 1  # Increment the next_id for the next journal entry
    return jsonify(new_entry), 201  # Return the newly created entry with a 201 (Created) status

# Route to retrieve all journal entries
@app.route('/journal', methods=['GET'])
def get_entries():
    """
    Handles GET requests to fetch all journal entries.
    - Returns the list of all journal entries stored in the `journal_entries` list.
    - Returns a JSON response containing the list of journal entries.
    """
    return jsonify(journal_entries)

# Route to update a specific journal entry
@app.route('/journal/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """
    Handles PUT requests to update an existing journal entry by its ID.
    - Accepts the entry ID as a URL parameter.
    - Extracts the new data (date and content) from the JSON body of the request.
    - Searches for the journal entry by its ID and updates it with the new data.
    - If the entry is found, it returns the updated entry as a JSON response.
    - If the entry is not found, it returns a 404 error with a message indicating that the entry was not found.
    """
    data = request.get_json()  # Get the updated data from the request body
    for entry in journal_entries:
        if entry['id'] == entry_id:  # Find the entry by its ID
            # Update the date and content with the provided data, if present
            entry['date'] = data.get('date', entry['date'])
            entry['content'] = data.get('content', entry['content'])
            return jsonify(entry)  # Return the updated entry as a JSON response
    return jsonify({'error': 'Entry not found'}), 404  # Return a 404 error if the entry was not found

# Route to delete a specific journal entry
@app.route('/journal/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """
    Handles DELETE requests to remove a specific journal entry by its ID.
    - Accepts the entry ID as a URL parameter.
    - Filters the journal entries list to remove the entry that matches the provided ID.
    - Returns a success message indicating that the entry has been deleted.
    """
    global journal_entries
    # Create a new list with all entries except the one to be deleted
    journal_entries = [entry for entry in journal_entries if entry['id'] != entry_id]
    return jsonify({'message': 'Entry has been deleted'}), 200  # Return a success message with HTTP status 200 (OK)

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
