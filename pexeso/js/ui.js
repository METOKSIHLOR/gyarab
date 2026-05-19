function render() {
    const board = document.getElementById("game-board")

    document.getElementById("score").textContent = `Score: ${userSettings.score}`

    if (board.children.length === 0) {
        cards.forEach(card => {
            const div = document.createElement("div")
            div.classList.add("card")
            div.dataset.id = card.id

            div.innerHTML = `
                <img class="front" src="imgs/${userSettings.mode}/${card.value}.jpg">
                <img class="back" src="imgs/card_back.jpg">
            `

            div.addEventListener("click", () => handleCardClick(card.id))
            board.appendChild(div)
        })
    }

    cards.forEach(card => {
        const div = board.querySelector(`[data-id="${card.id}"]`)
        if (!div) return

        if (card.selected || card.matched) {
            div.classList.add("flipped")
        } else {
            div.classList.remove("flipped")
        }

        if (card.matched) {
            div.style.visibility = "hidden"
            div.style.pointerEvents = "none"
        } else {
            div.style.visibility = "visible"
            div.style.pointerEvents = "auto"
        }
    })
}


function setSettings() {
    const inputElement = document.getElementById("pairsInput")

    const inputValue = inputElement.value.trim()

    const pairs = Number(inputValue)
    const mode = document.querySelector('input[name="mode"]:checked').value

    userSettings.mode = mode
    userSettings.pairs = pairs

    initGame()
    render()
}


function startGame() {
    const menu = document.getElementById("menu")
    const game = document.getElementById("game")

    menu.style.display = "none"
    game.style.display = "block"

    setSettings()
}

function mainMenu() {
    const menu = document.getElementById("menu")

    menu.innerHTML = `
     <h3>Pairs</h3>
    <input id="pairsInput" type="number" min="1" max="10" value="5">
    <h3>Mode</h3>
        <label class="radio-option">
            <span>Normal</span>
            <input type="radio" name="mode" value="normal" checked>
        </label>

        <label class="radio-option">
            <span>Pain</span>
            <input type="radio" name="mode" value="pain">
        </label>

        <button id="startBtn">Start</button>
        `

    const start = document.getElementById("startBtn")
    const input = document.getElementById("pairsInput");

    input.addEventListener('input', function() {
        this.value = this.value.replace(/\D/g, '')

        if (parseInt(this.value) > 10) {
            this.value = 10
        }
    })

    input.addEventListener('blur', function() {
        const val = parseInt(this.value);
        if (isNaN(val) || val < 1) {
            this.value = 5
        }
    })

    const radios = document.querySelectorAll('input[name="mode"]');

    radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === "pain") {
                input.value = 10
                input.disabled = true
            } else {
                input.disabled = false
                input.value = 5
            }
        })
    })
    start.addEventListener("click", () => startGame())
}

function reset() {
    userSettings.score = 0
    firstCard = null
    secondCard = null

    document.getElementById("game-board").innerHTML = ""

    initGame()
    render()
}
