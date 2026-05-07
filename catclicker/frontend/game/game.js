// Globální stav hry na straně klienta
let state = {
    points: 0,
    pps: 0, // Body za sekundu
    ppc: 1  // Body za kliknutí
}

// Seznam vylepšení - musí odpovídat seznamu na backendu
upgrades = [
    {"name": "Miska mléka", "cost": 15, "effect": {"pps": 1, "ppc": 0}},
    {"name": "Papírová krabice", "cost": 100, "effect": {"pps": 5, "ppc": 0}},
    {"name": "Gumová myš", "cost": 250, "effect": {"pps": 0, "ppc": 2}},

    {"name": "Škrabadlo Deluxe", "cost": 500, "effect": {"pps": 12, "ppc": 1}},
    {"name": "Catnip High Quality", "cost": 1200, "effect": {"pps": 25, "ppc": 0}},
    {"name": "Laserové ukazovátko", "cost": 3000, "effect": {"pps": 50, "ppc": 5}},

    {"name": "Automatické krmítko", "cost": 7500, "effect": {"pps": 120, "ppc": 0}},
    {"name": "Vyhřívaný pelíšek", "cost": 15000, "effect": {"pps": 250, "ppc": 10}},
    {"name": "Robotický vysavač", "cost": 50000, "effect": {"pps": 600, "ppc": 0}},

    {"name": "Kočičí kavárna", "cost": 150000, "effect": {"pps": 1500, "ppc": 50}},
    {"name": "Chrám bohyně Bastet", "cost": 500000, "effect": {"pps": 5000, "ppc": 100}},
    {"name": "Vesmírná stanice MIAU", "cost": 2000000, "effect": {"pps": 25000, "ppc": 500}},
]

// Logika pro vizuální změnu kočky (otevření/zavření pusy)
const catImg = document.querySelector('#cat-target img')
const normalSrc = "/static/game/imgs/cat_close.png"
const activeSrc = "/static/game/imgs/cat_open.png"

const startClick = () => {
    catImg.src = activeSrc;
};

const stopClick = () => {
    catImg.src = normalSrc;
};

// Event listenery pro animaci kliknutí a ošetření úniku myši z oblasti
document.getElementById("cat-target").addEventListener("mousedown", startClick)
document.getElementById("cat-target").addEventListener("mouseup", stopClick)
document.getElementById("cat-target").addEventListener("mouseleave", stopClick)

// Aktualizace UI prvků na stránce
function updateDisplay() {
    document.getElementById('points').innerText = Math.floor(state.points)
    document.getElementById('pps').innerText = state.pps
    document.getElementById('ppc').innerText = state.ppc
}

// Funkce pro nákup vylepšení přes API
async function buyUpgrade(name) {
    const response = await fetch("/api/game/upgrade/", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"name": name})
    })

    if (response.ok) {
        loadState() // Po nákupu obnovíme data ze serveru
    } else {
        alert("Nemáte tolik pointů")
    }
}

// Dynamické vykreslení tlačítek v obchodě
function renderUpgrades() {
    const list = document.getElementById("upgrades-list")
    list.innerHTML = ""
    upgrades.forEach(u => {
        const btn = document.createElement("button")
        btn.className = "upgrade-btn"

        // Formátování textu efektu (PPS/PPC)
        let effectText = "";
        if (u.effect.pps > 0) effectText += `+${u.effect.pps} PPS `;
        if (u.effect.ppc > 0) effectText += `+${u.effect.ppc} PPC`;

        btn.innerHTML = `
            <strong>${u.name}</strong><br>
            <span>Cost: ${u.cost} pts</span><br>
            <small>Effect: ${effectText}</small>
        `
        btn.onclick = () => buyUpgrade(u.name)
        list.appendChild(btn)
    })
}

// Správa modálního okna obchodu
const modal = document.getElementById('shopModal')

document.getElementById('openShopBtn').onclick = () => {
    modal.style.display = "block"
    renderUpgrades()
};

document.querySelector('.close-modal').onclick = () => modal.style.display = "none"

// Zavření modálu kliknutím mimo okno
window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

// Načtení celkového stavu uživatele a dopočítání bodů za dobu offline
async function loadState() {
    const response = await fetch('/api/users/profile/')
    if (response.status === 401) {
        window.location.href = '../login'
        return
    }
    const data = await response.json()

    // Synchronizace bodů se serverem (připočtení pasivního příjmu)
    const points_response = await fetch("/api/game/update_points/", {"method": "POST"})
    const points_data = await points_response.json()

    state.points = points_data.points
    state.pps = data.pps
    state.ppc = data.ppc
    updateDisplay()
}

// Odhlášení uživatele a přesměrování
document.getElementById("logout-btn").addEventListener("click", () => {
    fetch("/api/users/logout/", {"method": "DELETE"})
    window.location.href = '../login'
})

// Odeslání požadavku na kliknutí na server
document.getElementById("cat-target").addEventListener("click", async () => {
    const response = await fetch("/api/game/click/", {"method": "POST"})
    const data = await response.json()
    state.points = data.points
    updateDisplay()
})

// Inicializace hry při načtení stránky
window.onload = async () => {
    loadState()
}

// Interval pro vizuální přičítání bodů každou sekundu (pasivní příjem v UI)
setInterval(() => {
    state.points += state.pps
    updateDisplay()
}, 1000)
