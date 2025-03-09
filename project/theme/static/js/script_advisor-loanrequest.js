document.addEventListener("DOMContentLoaded", function () {
    const clientSelect = document.getElementById("clientSelect");
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");
    const tableBody = document.getElementById("tableBody");
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // CSRF sécurisé

    function filterAndSortTable() {
        let selectedClient = clientSelect.value;
        let start = startDate.value ? new Date(startDate.value) : null;
        let end = endDate.value ? new Date(endDate.value) : null;

        // Vider complètement le tableau avant de commencer le filtrage
        tableBody.innerHTML = "";

        // Récupérer toutes les lignes de la table
        let rows = Array.from(document.querySelectorAll("#tableBody tr"));

        // Filtrer les lignes selon le client sélectionné et les dates
        let filteredRows = rows.filter(row => {
            let clientId = row.getAttribute("data-client");
            let loanDateStr = row.getAttribute("data-date");

            if (!loanDateStr) {
                console.warn("Ligne ignorée car `data-date` est manquant :", row);
                return false; // Ignore les lignes sans date
            }

            let loanDate = new Date(loanDateStr);
            let clientMatch = (selectedClient === "" || clientId === selectedClient);
            let dateMatch = (!start || loanDate >= start) && (!end || loanDate <= end);

            return clientMatch && dateMatch;
        });

        // Trier les lignes par ID décroissant (du plus grand au plus petit)
        filteredRows.sort((a, b) => {
            let idA = parseInt(a.getAttribute("data-id")) || 0;
            let idB = parseInt(b.getAttribute("data-id")) || 0;
            return idB - idA; // Tri décroissant
        });

        // Ajouter les lignes filtrées et triées dans le tableau
        filteredRows.forEach(row => tableBody.appendChild(row));

        // Appliquer les événements sur les boutons après le filtrage
        applyStatusChangeEventListeners();
    }

    function updateStatus(loanId, status) {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        fetch(`/update_loan_status/${loanId}/`, {
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
                    let statusCell = document.getElementById("status-" + loanId);
                    statusCell.innerText = status;
                    statusCell.classList.add(status === "approved" ? "text-green-600" : "text-red-600");

                    if (statusCell.nextElementSibling) {
                        statusCell.nextElementSibling.innerHTML = "";
                    }
                } else {
                    alert("Error updating status!");
                }
            })
            .catch(error => console.error("Error:", error));
    }

    function applyStatusChangeEventListeners() {
        // Ajouter des écouteurs pour les boutons de mise à jour
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

    // Ajout des Event Listeners pour filtrer et trier les prêts
    clientSelect.addEventListener("change", filterAndSortTable);
    startDate.addEventListener("change", filterAndSortTable);
    endDate.addEventListener("change", filterAndSortTable);

    // Appliquer le tri et le filtrage au chargement de la page
    filterAndSortTable();
});
