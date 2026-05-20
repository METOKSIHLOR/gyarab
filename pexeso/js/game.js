const pairs_values = [1,2,3,4,5,6,7,8,9,10]

const userSettings = {
    pairs: 5,
    mode: "normal",
    score: 0
}

let cards = []
let firstCard = null
let secondCard = null
let id = 0

function setCardsArray() {
    const cards = []

    for (let i = 0; i < userSettings.pairs; i++) {
        let value = pairs_values[i]

        cards.push({id: id++, value, matched: false, selected: false})
        cards.push({id: id++, value, matched: false, selected: false})
    }

    return cards
}

function checkMatchCards() {
    if (firstCard.value === secondCard.value) {
        firstCard.matched = true
        secondCard.matched = true

        firstCard = null
        secondCard = null
        
        userSettings.score += 20

        let flag = true 
        for (let i = 0; i < cards.length; i++) {
            if (!cards[i].matched) {
                flag = false
            }
        }

        if (flag) {
            setTimeout(() => {
            alert("YOU WON!")
            document.getElementById("game-board").innerHTML = ""
            initGame()
            render()
            }, 500)
        }

    } else {
        userSettings.score > 0 ? userSettings.score -= 5 : 0
        setTimeout(() => {
            firstCard.selected = false
            secondCard.selected = false 

            firstCard = null
            secondCard = null

            render()
        }, 1500)
    }
}

function handleCardClick(id) {
    if (firstCard && secondCard) return

    const card = cards.find(c => c.id === id)
    if (card.matched || card.selected) return

    if (!firstCard) {
        firstCard = card 
        card.selected = true
    } else if (!secondCard) {

        secondCard = card
        card.selected = true

        checkMatchCards()
    }
    
    render()
}

function initGame() {
    id = 0
    cards = shuffle(setCardsArray())
}