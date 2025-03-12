document.addEventListener("DOMContentLoaded", function () {
    const clientSelect = document.getElementById("clientSelect");
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");
    const tableBody = document.getElementById("tableBody");
    const originalRows = Array.from(tableBody.getElementsByTagName("tr"));

    function filterAndSortTable() {
        const selectedClient = clientSelect.value;
        const start = startDate.value ? new Date(startDate.value) : null;
        const end = endDate.value ? new Date(endDate.value) : null;

        // Clear the table body
        tableBody.innerHTML = "";

        // Create a copy of the original rows for filtering
        let filteredRows = originalRows.filter(row => {
            const clientId = row.getAttribute("data-client");
            const loanDateStr = row.getAttribute("data-date");

            if (!loanDateStr) return false;

            const loanDate = new Date(loanDateStr);
            const clientMatch = !selectedClient || clientId === selectedClient;
            const dateMatch = (!start || loanDate >= start) && (!end || loanDate <= end);

            return clientMatch && dateMatch;
        });

        // Sort rows by ID (most recent first)
        filteredRows.sort((a, b) => {
            const idA = parseInt(a.getAttribute("data-id")) || 0;
            const idB = parseInt(b.getAttribute("data-id")) || 0;
            return idB - idA;
        });

        // Add filtered and sorted rows back to the table
        filteredRows.forEach(row => {
            // Create a clone of the row to avoid reference issues
            const newRow = row.cloneNode(true);
            tableBody.appendChild(newRow);
        });

        // Show "No results" message if no rows match
        if (filteredRows.length === 0) {
            const noResultsRow = document.createElement("tr");
            noResultsRow.innerHTML = `
                <td colspan="9" class="py-6 text-center text-gray-500">
                    No loan predictions available for the selected filters.
                </td>
            `;
            tableBody.appendChild(noResultsRow);
        }

        // Reapply event listeners to the new rows
        applyStatusChangeEventListeners();
    }

    function updateStatus(loanId, status) {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        fetch(`/update_prediction/${loanId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ status: status })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const statusCell = document.getElementById(`status-${loanId}`);
                    statusCell.innerText = status;
                    statusCell.className = `py-4 px-6 font-semibold ${status === "approved" ? "text-green-600" : "text-red-600"
                        }`;

                    // Remove action buttons after status update
                    const actionCell = statusCell.nextElementSibling;
                    if (actionCell) {
                        actionCell.innerHTML = "";
                    }
                } else {
                    alert("Error updating status!");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error updating status!");
            });
    }

    function applyStatusChangeEventListeners() {
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
    }

    // Add event listeners
    clientSelect.addEventListener("change", filterAndSortTable);
    startDate.addEventListener("change", filterAndSortTable);
    endDate.addEventListener("change", filterAndSortTable);

    // Store initial table state
    applyStatusChangeEventListeners();
});