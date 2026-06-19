function initBudget() {
    const saveButton     = document.getElementById("save");
    const categorySelect = document.getElementById("category");
    const limitInput     = document.getElementById("limit");

    if (!saveButton) return;

    saveButton.addEventListener("click", async () => {
        const categoryId = categorySelect.value;
        const amount     = limitInput.value;

        if (!categoryId) { alert("Please select a category."); return; }
        if (!amount || parseFloat(amount) <= 0) { alert("Please enter a valid amount."); return; }

        const response = await fetch("/budget", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ category_id: categoryId, amount }) 
        });

        response.ok ? loadSection("budget") : alert("Something went wrong. Please try again.");
    });

    document.querySelectorAll(".edit-budget").forEach(btn => {
        btn.addEventListener("click", async function () {
            const row        = this.closest("tr");
            const budgetId   = row.dataset.id;
            const amountCell = row.children[1];

            // Save the changed amount and send update request to the server
            if (this.classList.contains("btn-confirm-edit")) {
                const newAmount = parseFloat(row.querySelector(".edit-input").value);

                if (!newAmount || newAmount <= 0) { alert("Please enter a valid amount."); return; }

                const response = await fetch(`/budget/${budgetId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ amount: newAmount })
                });

                response.ok ? loadSection("budget") : alert("Could not update. Please try again.");
                return;
            }

            // EDIT MODE
            const currentAmount = amountCell.textContent.trim();
            // Replace amount text with an input field
            amountCell.innerHTML = `
                <input type="number" class="edit-input"
                value="${currentAmount}" min="0" step="0.01" style="width:120px">
            `;
            // Change edit button to confirm button
            this.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
            this.classList.replace("edit-budget", "btn-confirm-edit");

            const cancelBtn = document.createElement("button");
            cancelBtn.innerHTML = '<i class="fa-solid fa-circle-minus"></i>';
            cancelBtn.classList.add("btn", "btn-cancel-edit");
            this.insertAdjacentElement("afterend", cancelBtn);

            cancelBtn.addEventListener("click", () => {
                amountCell.textContent = currentAmount;
                this.innerHTML = '<i class="fa-regular fa-pen-to-square"></i>';
                this.classList.replace("btn-confirm-edit", "edit-budget");
                cancelBtn.remove();
            });
        });
    });

    document.querySelectorAll(".delete-budget").forEach(btn => {
        btn.addEventListener("click", async function () {
            if (!confirm("Delete this budget entry?")) return;

            const response = await fetch(`/budget/${this.dataset.id}`, {
                method: "DELETE"
            });

            response.ok ? loadSection("budget") : alert("Could not delete. Please try again.");
        });
    });
}