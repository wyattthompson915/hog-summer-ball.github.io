async function loadTable(jsonFile, tableId) {
    const response = await fetch(jsonFile);
    const data = await response.json();

    const table = document.getElementById(tableId);

    const headers = Object.keys(data[0]);

    const thead = table.createTHead();
    const headerRow = thead.insertRow();

    headers.forEach(header => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });

    const tbody = table.createTBody();

    data.forEach(row => {
        const tr = tbody.insertRow();

        headers.forEach(header => {
            const td = tr.insertCell();
            td.textContent = row[header];
        });
    });
}

loadTable("data/batters.json", "battingTable");
loadTable("data/pitchers.json", "pitchingTable");
loadTable("data/batters_ccl.json", "cclbattingTable");