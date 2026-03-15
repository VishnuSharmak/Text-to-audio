let currentAudio = null;

function convert() {
    const text = document.getElementById("text").value;
    const voice = document.getElementById("voice").value;

    fetch("/convert", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "text=" + encodeURIComponent(text) + "&voice=" + voice
    })
    .then(res => res.json())
    .then(data => {
        currentAudio = data.audio_url;
        alert("Audio created successfully!");
    });
}

function preview() {
    if (!currentAudio) {
        alert("Please convert text first!");
        return;
    }

    const audio = document.getElementById("player");
    audio.src = currentAudio;
    audio.style.display = "block";
    audio.play();
}

function downloadAudio() {
    if (!currentAudio) {
        alert("Please convert text first!");
        return;
    }

    window.location.href = "/download-audio";
}
