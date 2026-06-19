function initGoals() {
    const saveButton = document.getElementById("goals-save");
    if (!saveButton) return;

    const titleInput = document.getElementById("goals-title");
    const amountInput = document.getElementById("goals-amount");

    saveButton.addEventListener("click", async () => {
        const title = titleInput.value.trim();
        const targetAmount = parseFloat(amountInput.value);

        if (!title) {
            alert("Please enter a title.");
            return;
        }

        if (isNaN(targetAmount) || targetAmount <= 0) {
            alert("Please enter a valid target amount.");
            return;
        }

        const response = await fetch("/goals", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: title,
                target_amount: targetAmount
            })
        });

        response.ok ? loadSection("goals") : alert("Could not save goal.");
    });

    document.querySelectorAll("#goals-tbody tr").forEach(row => {
        const goalId = row.dataset.goalId;

        const titleInput = row.querySelector(".goal-title-input");
        const targetInput = row.querySelector(".goal-target-input");
        const statusSelect = row.querySelector(".goal-status-select");
        const editButton = row.querySelector(".edit-goal");
        const deleteButton = row.querySelector(".delete-goal");

        titleInput.disabled = true; // Initially disable inputs
        targetInput.disabled = true; // Initially disable inputs
 
        editButton.addEventListener("click", async function () {
            const isEditing = this.classList.contains("editing");

            if (!isEditing) {
                const oldTitle = titleInput.value;
                const oldTarget = targetInput.value;

                titleInput.disabled = false;
                targetInput.disabled = false;

                this.classList.add("editing");
                this.innerHTML = '<i class="fa-solid fa-circle-check"></i>';

                const cancelBtn = document.createElement("button");
                cancelBtn.innerHTML = '<i class="fa-solid fa-circle-minus"></i>';
                cancelBtn.classList.add("btn-cancel-edit");

                this.insertAdjacentElement("afterend", cancelBtn);

                cancelBtn.addEventListener("click", () => {
                    titleInput.value = oldTitle;
                    targetInput.value = oldTarget;

                    titleInput.disabled = true;
                    targetInput.disabled = true;

                    this.classList.remove("editing");
                    this.innerHTML = '<i class="fa-regular fa-pen-to-square"></i>';

                    cancelBtn.remove();
                });

                return;
            }

            const title = titleInput.value.trim();
            const targetAmount = parseFloat(targetInput.value);

            if (!title) {
                alert("Title cannot be empty.");
                return;
            }

            if (isNaN(targetAmount) || targetAmount <= 0) {
                alert("Please enter a valid target amount.");
                return;
            }

            const response = await fetch(`/goals/${goalId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: title,
                    target_amount: targetAmount
                })
            });

            response.ok ? loadSection("goals") : alert("Could not update goal.");
        });

        statusSelect.addEventListener("change", async function () {
            const response = await fetch(`/goals/${goalId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    status: statusSelect.value
                })
            });

            if (!response.ok) {
                alert("Could not update status.");
            }
        });

        deleteButton.addEventListener("click", async function () {
            if (!confirm("Delete this goal?")) return;

            const response = await fetch(`/goals/${goalId}`, {
                method: "DELETE"
            });

            response.ok ? loadSection("goals") : alert("Could not delete goal.");
        });
    });
}