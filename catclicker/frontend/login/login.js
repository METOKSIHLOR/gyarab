document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault()

    const formData = new FormData(e.target)
    const data = Object.fromEntries(formData.entries())
    const errorBox = document.getElementById('error-message')

    try {
        const response = await fetch('/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        const result = await response.json()

        if (response.ok) {
            window.location.href = '../game'
        } else {
            errorBox.innerText = result.name || result.error || 'Chyba přihlášení'
        }
    } catch (err) {
        errorBox.innerText = 'Server je nedostupný'
    }
})
