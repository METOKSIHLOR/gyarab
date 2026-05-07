let state = {
    points: 0,
    pps: 0,
    ppc: 1
}
const catImg = document.querySelector('#cat-target img')
const normalSrc = "/static/game/cat_close.png"
const activeSrc = "/static/game/cat_open.png"

document.getElementById("cat-target").addEventListener("mousedown", () => {
    catImg.src = activeSrc;
})

document.getElementById("cat-target").addEventListener("mouseup", () => {
    catImg.src = normalSrc
})

const upgrades = [
    {"name": "cat mint", "cost": 1, "effect": {"pps": 1, "ppc": 0}},
    {"name": "ball of thread", "cost": 100, "effect": {"pps": 0, "ppc": 1}},
    {"name": "scratching post", "cost": 300, "effect": {"pps": 3, "ppc": 1}},
    {"name": "cat bed", "cost": 500, "effect": {"pps": 3, "ppc": 3}},
    {"name": "cat hat", "cost": 1000, "effect": {"pps": 7, "ppc": 7}},
]
function updateDisplay() {
    document.getElementById('points').innerText = Math.floor(state.points)
    document.getElementById('pps').innerText = state.pps
    document.getElementById('ppc').innerText = state.ppc
}

async function buyUpgrade(name) {
    const response= await fetch("/api/game/upgrade/",
        {method: "POST",
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({"name": name})})

    if (response.ok) {
        loadState()
    } else {
        alert("Nemáte tolik pointů")
    }
}


function renderUpgrades() {
    const list = document.getElementById("upgrades-list")
    list.innerHTML = ""
    upgrades.forEach(u => {
        const btn = document.createElement("button")
        btn.className = "upgrade-btn"
        btn.innerHTML = `${u.name} (${u.cost} pts) <br> <small>${u.effect}</small>`
        btn.onclick = () => buyUpgrade(u.name)
        list.appendChild(btn)
    })
}

const modal = document.getElementById('shopModal')

document.getElementById('openShopBtn').onclick = () => {
    modal.style.display = "block"
    renderUpgrades()
};
document.querySelector('.close-modal').onclick = () => modal.style.display = "none"

window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
async function loadState() {
    const response = await fetch('/api/users/profile/')
    if (response.status === 401) {
        window.location.href = '../login'
        return
    }
    const data = await response.json()
    state.points = data.points
    state.pps = data.pps
    state.ppc = data.ppc
    updateDisplay()
}

document.getElementById("logout-btn").addEventListener("click", () => {
    const response = fetch("/api/users/logout/", {"method": "DELETE"})
    window.location.href = '../login'
})

document.getElementById("cat-target").addEventListener("click", async () => {
    const response = await fetch("/api/game/click/", {"method": "POST"})
    const data = await response.json()
    state.points = data.points
    updateDisplay()
})

loadState()

setInterval(() => {
    state.points += state.pps
    updateDisplay()
},1000)