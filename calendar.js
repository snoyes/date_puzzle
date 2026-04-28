function pad(n) {
    return n.toString().padStart(2, '0');
}

async function loadFile() {

    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    const weekday = document.getElementById('weekday').value;

    const container = document.getElementById('container')
    const message = document.getElementById('message')

    if (month === '' || day === '' || weekday === '') return;

    const filename = `results/${pad(month)}${pad(day)}${weekday}.txt`;

    message.innerHTML = "Loading...";

    try {
        const response = await fetch(filename);
        if (!response.ok) throw new Error('File not found');

        message.innerHTML = "Rendering...";
        const text = await response.text();
        container.innerHTML = text;
        render();
        message.innerHTML = "";
    } catch (e) {
        message.innerHTML = `Error loading ${filename}`;
    }
}

function render() {
    const inputText = document.getElementById('container').innerHTML.trim();
    const outputDiv = document.getElementById('container');

    let formattedHtml = '';

    const lines = inputText.split('\n');

    lines.forEach(line => {
        let lineHtml = '';
        for (let i = 0; i < line.length; i++) {
            // Wrap each character in a <span> tag
            lineHtml += `<span class="b${line[i]}">${line[i]}</span>`;

            // Insert a <br> tag after every 7th character
            // Ensure it's not the last character of the line
            if ((i + 1) % 7 === 0 && (i + 1) < line.length) {
                lineHtml += `<br>`;
            }
        }
        formattedHtml += `<div>${lineHtml}</div>`;
    });

    outputDiv.innerHTML = formattedHtml;
}

window.onload = function() {
    const now = new Date();

    // Month: 1–12
    const month = now.getMonth() + 1;

    // Day: 1–31
    const day = now.getDate();

    // Weekday: convert JS (0=Sun..6=Sat) → (0=Mon..6=Sun)
    const jsDay = now.getDay();
    const weekday = (jsDay + 6) % 7;

    document.getElementById('month').value = month;
    document.getElementById('day').value = day;
    document.getElementById('weekday').value = weekday;

    loadFile();
};
