document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault()

    const formData = new FormData(e.target)
    const data = Object.fromEntries(formData.entries())
    const errorBox = document.getElementById('error-message')

    try {
        const response = await fetch('/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        const result = await response.json()

        if (response.ok) {
            window.location.href = '../login'
        } else {
            errorBox.innerText = result.name || result.error || 'Chyba při registraci'
        }
    } catch (err) {
        errorBox.innerText = 'Server je nedostupný'
    }
});
