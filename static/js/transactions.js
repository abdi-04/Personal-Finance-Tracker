function initTransactions() {
    const saveButton = document.getElementById("txn-save");
    if (!saveButton) return;

    const categorySelect   = document.getElementById("txn-category");
    const amountInput      = document.getElementById("txn-amount");
    const descriptionInput = document.getElementById("txn-description");
    const dateInput        = document.getElementById("txn-date");
    const searchInput      = document.getElementById("txn-search");
    const sortField  = document.getElementById("txn-sort-field");
    const sortDirSel = document.getElementById("txn-sort-dir");

    /*Default Date*/
    if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split("T")[0];
    }

    /*Save Transaction*/
    saveButton.addEventListener("click", async () => {
        const categoryId  = categorySelect.value || null;
        const amount      = parseFloat(amountInput.value);
        const description = descriptionInput.value.trim();
        const date        = dateInput.value;

        if (!amount || amount <= 0) {
            alert("Please enter a valid amount.");
            return;
        }

        if (!date) {
            alert("Please select a date.");
            return;
        }

        // sends a request to the server to save a transaction
        const response = await fetch("/transactions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                category_id: 
                categoryId, 
                amount, 
                description, 
                date })
        });

        if (response.ok) {
            loadSection("transactions");
        } else {
            alert("Something went wrong. Please try again.");
        }
    });

    /*Delete Transaction*/
    document.querySelectorAll(".delete-txn").forEach(btn => {
        btn.addEventListener("click", async function () {
            if (!confirm("Delete this transaction?")) return;

            // retrieve the transaction id of the row (comes from html)
            // dataset = builtin browser object. Gives me data-*, * = id
            const txnId = this.dataset.id;

            const response = await fetch(`/transactions/${txnId}`, {
                method: "DELETE"
            });

            if (response.ok){
                loadSection("transactions");
            } else {
                alert("Could not delete. Please try again.");
            }
        });
    });

    /*Search Filter*/
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase().trim();
            filterTable(query);
        });
    }

    function filterTable(query) {
        document.querySelectorAll("#txn-tbody tr").forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(query)) {
                row.style.display = ""; // show row
            } else {
                row.style.display = "none"; //hide row
            }
            
        });
    }

    /*Edit Transaction*/
    document.querySelectorAll(".edit-txn").forEach(btn => {
        // Attach a click listener to every edit button on the page
        btn.addEventListener("click", async function () {
            // lets us grap the id of the row from the the nearest <tr>
            const row = this.closest("tr");
            const txnId = row.dataset.id;
            const amountCell = row.querySelector(".amountcell-trans");

            // EDIT MODE — runs when the edit (pen) button is clicked
            if (this.classList.contains("edit-txn")) {
                 // Read the current amount text from the cell and remove any whitespace
                const currentAmount = amountCell.textContent.trim();

                // Replace the amount text with an input field so the user can type a new value
                amountCell.innerHTML = `
                    <input type="number" class="edit-input" value="${currentAmount}" min="0" step="0.01" style="width:120px">
                `;

                // Change the edit (pen) icon to a confirm (checkmark) icon
                this.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                // Swap the button's class from "edit-txn" to "btn-confirm-edit"
                // so the next click goes into SAVE MODE instead of EDIT MODE
                this.classList.replace("edit-txn", "btn-confirm-edit");

                // Create a new cancel button element
                const cancelBtn = document.createElement("button");
                // Give the cancel button a minus icon
                cancelBtn.innerHTML = '<i class="fa-solid fa-circle-minus"></i>';
                // Add CSS classes to the cancel button for styling
                cancelBtn.classList.add("btn", "btn-cancel-edit");
                // Insert the cancel button directly after the confirm button in the HTML
                this.insertAdjacentElement("afterend", cancelBtn);

                // restoring the original amount if cancel button is clicked
                cancelBtn.addEventListener("click", () => {
                    amountCell.textContent = parseFloat(currentAmount).toFixed(2);
                    this.innerHTML = '<i class="fa-regular fa-pen-to-square"></i>';
                    this.classList.replace("btn-confirm-edit", "edit-txn");
                    cancelBtn.remove();
                });

            }
            // If comfirm button is clicked, we send a request to the server for saving
            // the new amount
            else if (this.classList.contains("btn-confirm-edit")) {
                const input = row.querySelector(".edit-input");
                const newAmount = parseFloat(input.value);

                if (!newAmount || newAmount <= 0) {
                    alert("Please enter a valid amount.");
                    return;
                }

                const response = await fetch(`/transactions/${txnId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ amount: newAmount })
                });

                if (response.ok) {
                    loadSection("transactions");
                } else {
                    alert("Could not update. Please try again.");
                }
            }

        });      
    });

    // Sort Transactions 
    // Restore saved preferences 
    /* check if there is anything in local storage and set that as default otherwise
    use date and asc */
    if (sortField)  sortField.value  = localStorage.getItem("txn-sort-field") || "date";
    if (sortDirSel) sortDirSel.value = localStorage.getItem("txn-sort-dir")   || "asc";

    function sortTable(){
        
        const field = sortField.value; // get the value of the selected sort field
        const sortAsc = sortDirSel.value === "asc"; // determine if sorting in ascending order


        // set the current sort preferences in local storage 
        // so they persist on page reload
        localStorage.setItem("txn-sort-field", field);
        localStorage.setItem("txn-sort-dir", sortDirSel.value);

        // Get all the rows from the transaction table body and convert the NodeList to an array
        const rows = Array.from(document.querySelectorAll("#txn-tbody tr"));     

        // Sort the rows array based on the selected field and direction
        rows.sort((a, b) => {
            //
            let valA, valB;

            if (field === "date") {
                valA = a.cells[0].textContent.trim();
                valB = b.cells[0].textContent.trim();
            } else if (field === "category") {
                valA = a.cells[1].textContent.trim().toLowerCase();
                valB = b.cells[1].textContent.trim().toLowerCase();
            } else if (field === "amount") {
                valA = parseFloat(a.querySelector(".amountcell-trans").textContent);
                valB = parseFloat(b.querySelector(".amountcell-trans").textContent);
            }
            if(valA < valB) {
                if (sortAsc) {
                    return -1;  // A come before B
                } else {
                    return 1; // B comes before A
                }
            }
            // the oppsite the previous if statement (uses ternary operator)
            if (valA > valB) {
                if (sortAsc) {
                    return 1; // B comes before A
                } else {
                    return -1; // A come before B
                }
            }
            return 0; // A and B are equal, maintain original order
            })
        const tbody = document.getElementById("txn-tbody")
        rows.forEach(row => tbody.appendChild(row));
    }
    // Apply saved sort immediately on load
    sortTable();

    if (sortField)  sortField.addEventListener("change", sortTable);
    if (sortDirSel) sortDirSel.addEventListener("change", sortTable);




        /* Upload Receipt */
    const uploadBtn = document.getElementById("upload-receipt-btn");

    if (uploadBtn) {
        uploadBtn.addEventListener("click", async () => {

            const txnId = document.getElementById("upload-txn-id").value;
            const fileInput = document.getElementById("receipt-file");

            if (!txnId) {
                alert("Please select a transaction");
                return;
            }

            if (!fileInput.files.length) {
                alert("Please select a file");
                return;
            }

            const formData = new FormData();
            // "image" is the key that the server will look for when processing the upload
            // fileInput.files is a FileList object, we take the first file with [0]
            formData.append("image", fileInput.files[0]); 

            try {
                // Sends a request to the server to save the uploaded picture
                const res = await fetch(`/transactions/${txnId}/receipt`, {
                    method: "POST",
                    body: formData
                });
                
                if (!res.ok) {
                alert("Upload failed. Server error.");
                return;
                }

                const data = await res.json();

                if (data.success) {
                    alert("Receipt uploaded ");
                    loadSection("transactions"); // refresh
                } else {
                    alert(data.error || "Upload failed");
                }

            } catch (err) {
                console.error(err);
                alert("Something went wrong");
            }
        });
    }

}
