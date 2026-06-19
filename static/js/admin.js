//// User Management & Category Management 

function initAdmin() {

    //// Delete user 

    // Find every delete button in the user table and attach a click handler
    document.querySelectorAll(".delete-user").forEach(btn => {
        btn.addEventListener("click", async function () {
            // Walk up the DOM to find the <tr> that contains this button
            const row = this.closest("tr");

            // Read the user ID we stored on the row as a data attribute
            const userId = row.dataset.userId;

            // Guard: if there's somehow no ID, bail out early
            if (!userId) { alert("Invalid user."); return; }

            // Ask the user to confirm before doing anything destructive
            if (!confirm("Are you sure you want to delete this user account?")) return;

            try {
                // Send a DELETE request to the server for this specific user
                const response = await fetch(`/admin/${userId}`, { method: "DELETE" });

                if (response.ok) {
                    // Remove the row from the table so the UI updates instantly
                    row.remove();
                    alert("User deleted successfully.");
                } else {
                    // Parse the error message from the server response
                    const data = await response.json();
                    alert(data.error || "Could not delete user.");
                }
            } catch (err) {
                // This only fires if there was a network failure, not a server error
                console.error(err);
                alert("An unexpected error occurred.");
            }
        });
    });

    //// Category Management 

    // Grab the "Add category" button and the two inputs next to it
    const addBtn       = document.getElementById("addCategoryBtn");
    const nameInput    = document.getElementById("newCategoryName");
    const typeSelect   = document.getElementById("newCategoryType");
    const categoryBody = document.getElementById("categoryTableBody");

    // Guard: if the add button doesn't exist on this page, stop here
    if (!addBtn) return;

    //// Add 

    addBtn.addEventListener("click", async () => {
        // Read and trim whitespace from the name field
        const name = nameInput.value.trim();
        const type = typeSelect.value;

        // Don't submit if the name field is empty
        if (!name) return;

        try {
            // POST the new category to the server
            const response = await fetch("/categories", {
                method: "POST",
                // telling the server data type
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, type })
            });

            if (response.ok) {
                // Reload the page so the server re-renders the full updated table
                location.reload();
            } else {
                const data = await response.json();
                alert(data.error || "Could not add category.");
            }
        } catch (err) {
            console.error(err);
            alert("An unexpected error occurred.");
        }
    });

    //// Edit / Save / Delete (event delegation) 
    // Instead of attaching listeners to every button, we listen on the parent
    // tbody and check which button was actually clicked. This also works for
    // rows that are added dynamically after the page loads.

    categoryBody.addEventListener("click", async function (event) {
        // Find the row the clicked element belongs to
        const row = event.target.closest("tr");
        if (!row) return;

        // IMPORTANT: the cancel button is inside the tbody, so its clicks bubble
        // up here too. We must bail out early or the save handler below will also
        // fire on the same click event.
        if (event.target.closest(".cancel-category-btn")) return;

        // Read the category ID stored on the row
        const categoryId = row.dataset.categoryId;


        //// Edit clicked: switch the row into edit mode
        if (event.target.closest(".edit-category-btn")) {
            const editBtn = row.querySelector(".edit-category-btn");

            // Hide the read-only spans and reveal the editable inputs
            row.querySelector(".cat-display-name").classList.add("hidden");
            row.querySelector(".cat-display-type").classList.add("hidden");
            row.querySelector(".cat-edit-name").classList.remove("hidden");
            row.querySelector(".cat-edit-type").classList.remove("hidden");

            // Swap the edit icon for a save icon
            editBtn.innerHTML = '<i class="fa-solid fa-circle-plus"></i>';
            editBtn.classList.replace("edit-category-btn", "save-category-btn");

            // Create a cancel button and insert it right after the save button
            const cancelBtn = document.createElement("button");
            cancelBtn.innerHTML = '<i class="fa-solid fa-circle-minus"></i>';
            cancelBtn.classList.add("cancel-category-btn");
            editBtn.insertAdjacentElement("afterend", cancelBtn);

            // When cancel is clicked, restore the row to its read-only state
            cancelBtn.addEventListener("click", () => {
                // Show the read-only spans and hide the inputs again
                row.querySelector(".cat-display-name").classList.remove("hidden");
                row.querySelector(".cat-display-type").classList.remove("hidden");
                row.querySelector(".cat-edit-name").classList.add("hidden");
                row.querySelector(".cat-edit-type").classList.add("hidden");

                // Swap the save icon back to the edit icon
                editBtn.innerHTML = '<i class="fa-regular fa-pen-to-square"></i>';
                editBtn.classList.replace("save-category-btn", "edit-category-btn");

                // Remove the cancel button itself
                cancelBtn.remove();
            });

            return;
        }


        //// Save clicked: send the updated values to the server
        if (event.target.closest(".save-category-btn")) {
            const saveBtn = row.querySelector(".save-category-btn");
            const name    = row.querySelector(".cat-edit-name").value.trim();
            const type    = row.querySelector(".cat-edit-type").value;

            // Don't save if the name was left empty
            if (!name) return;

            try {
                // PUT the updated name and type to the server
                const response = await fetch(`/categories/${categoryId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, type })
                });

                if (response.ok) {
                    // Update the read-only spans with the newly saved values
                    row.querySelector(".cat-display-name").textContent = name;
                    row.querySelector(".cat-display-type").innerHTML   =
                        `<span class="type-badge ${type}">${type}</span>`;

                    // Show the read-only spans and hide the inputs again
                    row.querySelector(".cat-display-name").classList.remove("hidden");
                    row.querySelector(".cat-display-type").classList.remove("hidden");
                    row.querySelector(".cat-edit-name").classList.add("hidden");
                    row.querySelector(".cat-edit-type").classList.add("hidden");

                    // Swap the save icon back to the edit icon
                    saveBtn.innerHTML = '<i class="fa-regular fa-pen-to-square"></i>';
                    saveBtn.classList.replace("save-category-btn", "edit-category-btn");

                    // Remove the cancel button now that we're done editing
                    const cancelBtn = row.querySelector(".cancel-category-btn");
                    if (cancelBtn) cancelBtn.remove();
                } else {
                    const data = await response.json();
                    alert(data.error || "Could not update category.");
                }
            } catch (err) {
                console.error(err);
                alert("An unexpected error occurred.");
            }

            return;
        }


        //// Delete clicked: remove the category after confirmation 
        if (event.target.closest(".delete-category-btn")) {
            if (!confirm("Delete this category? Existing transactions will become uncategorized.")) return;

            try {
                // Send a DELETE request to the server for this category
                const response = await fetch(`/categories/${categoryId}`, { 
                    method: "DELETE" 
                });

                if (response.ok) {
                    // Remove the row from the table immediately
                    row.remove();
                } else {
                    alert("Could not delete category.");
                }
            } catch (err) {
                console.error(err);
                alert("An unexpected error occurred.");
            }
        }
    });

} 


// Wait until the full page HTML is loaded before running anything
document.addEventListener("DOMContentLoaded", () => {
    initAdmin(); // Set up all user and category handlers
});