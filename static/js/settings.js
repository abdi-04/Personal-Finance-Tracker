function initSettings() {
    const updateBtn = document.getElementById("update-password-btn");
    if (!updateBtn) return;

    updateBtn.addEventListener("click", async () => {
        const newPassword = document.getElementById("new-password").value.trim();
        const confirmPassword = document.getElementById("confirm-password").value.trim();

        if (!newPassword || !confirmPassword) {
            alert("Please fill in both password fields.");
            return;
        }

        const response = await fetch("/settings", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                new_password: newPassword,
                confirm_password: confirmPassword
            })
        });

        if (response.ok) {
            alert("Password updated successfully.");
            loadSection("settings");
        } else {
            const data = await response.json();
            alert(data.error || "Could not update password.");
        }
    });
}