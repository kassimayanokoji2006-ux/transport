document.addEventListener("DOMContentLoaded", function () {
    const ROWS_PER_PAGE = 5;

    function setupPagination(container) {
        if (!container) return;
        const targetId = container.getAttribute("data-target");
        const tbody = document.getElementById(targetId);
        if (!tbody) return;
        const pageInfo = container.querySelector('.pageInfo');
        const prevBtn = container.querySelector('.prev');
        const nextBtn = container.querySelector('.next');

        let currentPage = 1;
        function displayPage(page) {
            const rows = Array.from(tbody.getElementsByTagName("tr"));
            const totalPages = Math.max(1, Math.ceil(rows.length / ROWS_PER_PAGE));
            rows.forEach((row, idx) => {
                const start = (page - 1) * ROWS_PER_PAGE;
                const end = start + ROWS_PER_PAGE;
                row.style.display = (idx >= start && idx < end) ? "" : "none";
            });
            if (pageInfo) pageInfo.textContent = `Page ${page} sur ${Math.ceil(rows.length / ROWS_PER_PAGE) || 1}`;
            if (prevBtn) prevBtn.disabled = page === 1;
            if (nextBtn) nextBtn.disabled = page >= Math.ceil(rows.length / ROWS_PER_PAGE);
            currentPage = Math.min(page, Math.ceil(rows.length / ROWS_PER_PAGE) || 1);
        }
        if (prevBtn) prevBtn.addEventListener('click', () => { if (currentPage > 1) displayPage(currentPage - 1); });
        if (nextBtn) nextBtn.addEventListener('click', () => { displayPage(currentPage + 1); });
        displayPage(1);
    }

    function showMessage(message, type = 'info') {
        alert(message); // simple fallback; could be replaced by a toast UI
    }

    function enhanceDeletes() {
        document.querySelectorAll('a.row-delete').forEach((link) => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const url = new URL(this.href, window.location.origin);
                url.searchParams.set('ajax', '1');
                fetch(url.toString(), { method: 'GET' })
                    .then((res) => {
                        if (!res.ok) throw new Error('Suppression échouée');
                        return res.json();
                    })
                    .then(() => {
                        const row = this.closest('tr');
                        if (row) row.parentElement.removeChild(row);
                        showMessage('Suppression réussie', 'success');
                        // refresh pagination for all containers
                        document.querySelectorAll('.pagination-container').forEach(setupPagination);
                    })
                    .catch((err) => {
                        showMessage(`Erreur: ${err.message}`, 'error');
                    });
            });
        });
    }

    function rowClickToForm() {
        const pageEntity = document.querySelector('table[data-entity]');
        if (!pageEntity) return;
        const entity = pageEntity.getAttribute('data-entity');
        if (entity === 'etudiant') {
            const tbody = document.getElementById('studentTable');
            const form = document.getElementById('studentForm');
            const updateBtn = document.getElementById('updateStudentBtn');
            if (tbody && form && updateBtn) {
                tbody.addEventListener('click', function (e) {
                    const row = e.target.closest('tr');
                    if (!row) return;
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 7) {
                        form.id_eleve.value = cells[0].textContent.trim();
                        form.nom.value = cells[1].textContent.trim();
                        form.prenom.value = cells[2].textContent.trim();
                        form.date_naissance.value = cells[3].textContent.trim();
                        form.classe.value = cells[4].textContent.trim();
                        form.adresse.value = cells[5].textContent.trim();
                        form.tel_parent.value = cells[6].textContent.trim();
                        updateBtn.style.display = '';
                    }
                });
                updateBtn.addEventListener('click', function () {
                    const formData = new URLSearchParams(new FormData(form)).toString();
                    fetch('/views/etudiant/update', {
                        method: 'POST',
                        headers: { 'content-type': 'application/x-www-form-urlencoded' },
                        body: formData,
                    })
                        .then((res) => res.json())
                        .then((json) => {
                            if (!json.success) throw new Error(json.error || 'Erreur de mise à jour');
                            showMessage('Étudiant mis à jour', 'success');
                        })
                        .catch((err) => showMessage(`Erreur: ${err.message}`, 'error'));
                });
            }
        } else if (entity === 'bus') {
            const tbody = document.getElementById('vehicleTable');
            const form = document.querySelector('form[action="/views/bus/insert"]');
            const updateBtnId = 'updateBusBtn';
            let updateBtn = document.getElementById(updateBtnId);
            if (tbody && form) {
                if (!updateBtn) {
                    updateBtn = document.createElement('button');
                    updateBtn.id = updateBtnId;
                    updateBtn.type = 'button';
                    updateBtn.textContent = 'Modifier';
                    updateBtn.style.display = 'none';
                    form.appendChild(updateBtn);
                }
                tbody.addEventListener('click', function (e) {
                    const row = e.target.closest('tr');
                    if (!row) return;
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 4) {
                        form.idVehicule.value = cells[0].textContent.trim();
                        form.matricule.value = cells[1].textContent.trim();
                        form.marque.value = cells[2].textContent.trim();
                        form.capacite.value = cells[3].textContent.trim();
                        updateBtn.style.display = '';
                    }
                });
                updateBtn.addEventListener('click', function () {
                    const formData = new URLSearchParams(new FormData(form)).toString();
                    fetch('/views/bus/update', {
                        method: 'POST',
                        headers: { 'content-type': 'application/x-www-form-urlencoded' },
                        body: formData,
                    })
                        .then((res) => res.json())
                        .then((json) => {
                            if (!json.success) throw new Error(json.error || 'Erreur de mise à jour');
                            showMessage('Bus mis à jour', 'success');
                        })
                        .catch((err) => showMessage(`Erreur: ${err.message}`, 'error'));
                });
            }
        } else if (entity === 'transport') {
            const tbody = document.getElementById('transportTable');
            const form = document.getElementById('transportForm');
            const updateBtn = document.getElementById('updateTransportBtn');
            if (tbody && form && updateBtn) {
                tbody.addEventListener('click', function (e) {
                    const row = e.target.closest('tr');
                    if (!row) return;
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 4) {
                        form.refTrans.value = cells[0].textContent.trim();
                        form.dateTrans.value = cells[1].textContent.trim();
                        form.idEleve.value = (cells[2].dataset?.id || '').trim();
                        form.idVehicule.value = (cells[3].dataset?.id || '').trim();
                        updateBtn.style.display = '';
                    }
                });
                updateBtn.addEventListener('click', function () {
                    const formData = new URLSearchParams(new FormData(form)).toString();
                    fetch('/views/transports/update', {
                        method: 'POST',
                        headers: { 'content-type': 'application/x-www-form-urlencoded' },
                        body: formData,
                    })
                        .then((res) => res.json())
                        .then((json) => {
                            if (!json.success) throw new Error(json.error || 'Erreur de mise à jour');
                            showMessage('Transport mis à jour', 'success');
                        })
                        .catch((err) => showMessage(`Erreur: ${err.message}`, 'error'));
                });
            }
        }
    }

    function setupSearch(inputId, tbodyId) {
        const input = document.getElementById(inputId);
        const tbody = document.getElementById(tbodyId);
        if (!input || !tbody) return;
        const queryDisplay = document.getElementById(inputId.replace('Search','Query'));
        input.addEventListener('input', () => {
            const q = input.value.toLowerCase().trim();
            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.forEach((tr) => {
                const text = tr.textContent.toLowerCase();
                tr.style.display = text.includes(q) ? '' : 'none';
            });
            // Rebuild pagination for the container referencing this tbody
            const container = document.querySelector(`.pagination-container[data-target="${tbodyId}"]`);
            if (container) setupPagination(container);
            if (queryDisplay) queryDisplay.textContent = q ? `Recherche: ${q}` : '';
        });
    }

    // Table hover effect
    document.querySelectorAll('table tbody').forEach((tbody) => {
        tbody.addEventListener('mouseover', (e) => {
            const tr = e.target.closest('tr');
            if (tr) tr.classList.add('row-hover');
        });
        tbody.addEventListener('mouseout', (e) => {
            const tr = e.target.closest('tr');
            if (tr) tr.classList.remove('row-hover');
        });
    });

    // Setup
    document.querySelectorAll('.pagination-container').forEach(setupPagination);
    enhanceDeletes();
    rowClickToForm();
    // Searches per page
    setupSearch('studentSearch', 'studentTable');
    setupSearch('busSearch', 'vehicleTable');
    setupSearch('transportSearch', 'transportTable');
});