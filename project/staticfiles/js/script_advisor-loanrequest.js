document.addEventListener("DOMContentLoaded", function () {
    const clientSelect = document.getElementById("clientSelect");
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");
    const tableBody = document.getElementById("tableBody");

    function filterTable() {
        let selectedClient = clientSelect.value;
        let start = startDate.value ? new Date(startDate.value) : null;
        let end = endDate.value ? new Date(endDate.value) : null;

        let rows = tableBody.getElementsByTagName("tr");

        for (let row of rows) {
            let clientId = row.getAttribute("data-client");
            let loanDateStr = row.getAttribute("data-date");

            if (!loanDateStr) continue; // Ignore rows without a date

            let loanDate = new Date(loanDateStr);
            let clientMatch = (selectedClient === "" || clientId === selectedClient);
            let dateMatch = (!start || loanDate >= start) && (!end || loanDate <= end);

            row.style.display = (clientMatch && dateMatch) ? "" : "none";
        }
    }

    function updateStatus(loanId, status) {
        fetch(`/update_prediction/${loanId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify({ status: status })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let statusCell = document.getElementById("status-" + loanId);
                    statusCell.innerText = status;
                    statusCell.classList.remove("text-gray-600", "text-green-600", "text-red-600");
                    statusCell.classList.add(status === "approved" ? "text-green-600" : "text-red-600");

                    // Remove action buttons after update
                    let actionCell = statusCell.nextElementSibling;
                    if (actionCell) {
                        actionCell.innerHTML = "";
                    }
                } else {
                    alert("Error updating status!");
                }
            })
            .catch(error => console.error("Error:", error));
    }

    // Event listeners for filtering
    clientSelect.addEventListener("change", filterTable);
    startDate.addEventListener("change", filterTable);
    endDate.addEventListener("change", filterTable);

    // Event listeners for status update buttons
    document.querySelectorAll(".approve-btn").forEach(button => {
        button.addEventListener("click", function () {
            updateStatus(this.dataset.id, "approved");
        });
    });

    document.querySelectorAll(".reject-btn").forEach(button => {
        button.addEventListener("click", function () {
            updateStatus(this.dataset.id, "rejected");
        });
    });

    // Apply filtering on initial load
    filterTable();
});
