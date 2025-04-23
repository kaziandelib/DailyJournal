$(document).ready(function(){
    // Function to load all journal entries from the server and display them in the list
    function loadJournalEntries(){
        $.get('/journal', function(entries){
            // Clear the existing journal list to prevent duplication
            $('#journal-list').empty(); 

            // Loop through each journal entry and append it to the list
            entries.forEach(function(entry){
                $("#journal-list").append(`
                    <li class="flex justify-between" data-id="${entry.id}">
                        <div class="entry">
                            <strong>${entry.date}</strong>: ${entry.content}
                        </div>
                        <div class="buttons">
                            <button class="edit-btn">Edit</button>
                            <button class="delete-btn text-red">Delete</button>
                        </div>
                    </li>
                `);
            });
        });
    }

    // Call the loadJournalEntries function to populate the journal list when the page loads
    loadJournalEntries();

    // Event handler for the form submission to add a new journal entry
    $("#journal-form").on('submit', function(e){
        e.preventDefault();  // Prevent the default form submission behavior
        const newEntry = {
            date : $("#date").val(), // Get the value of the date input field
            content: $("#content").val(), // Get the value of the content textarea
        };

        // Make an AJAX POST request to add the new entry to the server
        $.ajax({
            url: '/journal',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(newEntry), // Convert the new entry to a JSON string
            success: function() {
                loadJournalEntries(); // Reload the journal entries after successful addition
                $("#journal-form")[0].reset(); // Reset the form fields after submitting
            }
        });
    });

    // Event handler for the edit button to update an existing journal entry
    $(document).on('click', '.edit-btn', function(){
        const li = $(this).closest('li');  // Get the closest <li> element to the clicked edit button
        const entryId = li.attr('data-id');  // Get the ID of the journal entry from the data-id attribute
        // Prompt the user to enter a new date and content for the journal entry
        const newDate = prompt("Enter new date: ", li.find('strong').text());
        const newContent = prompt("Enter new content: ", li.find('.entry').contents().filter(function(){
            return this.nodeType === 3; // Get the text content from the entry div
        }).text().trim());

        // If both the new date and content are provided, update the entry
        if (newDate && newContent){
            // Make an AJAX PUT request to update the entry on the server
            $.ajax({
                url: '/journal/' + entryId, // Use the entry ID in the URL to specify which entry to update
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({date: newDate, content: newContent}), // Send the updated date and content
                success: function(){
                    loadJournalEntries(); // Reload the journal entries after the update
                }
            });
        }
    });

    // Event handler for the delete button to remove a journal entry
    $(document).on('click', '.delete-btn', function(){
        const entryId = $(this).closest('li').attr('data-id');  // Get the ID of the entry to delete
        // Confirm with the user before deleting the entry
        if (confirm("Are you sure you want to delete this entry?")){
            // Make an AJAX DELETE request to remove the entry from the server
            $.ajax({
                url: '/journal/' + entryId, // Use the entry ID in the URL to specify which entry to delete
                method: 'DELETE',
                success: function(){
                    loadJournalEntries(); // Reload the journal entries after the deletion
                }
            });
        }
    });
});
