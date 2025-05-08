async function handleSubmit(event) {
    event.preventDefault()
    let src = event.srcElement
    let form = src.closest(".words")
    let word1span = form.querySelector(".word1")
    let word2input = form.querySelector(".word2")
    let word1 = word1span.textContent
    let word2 = word2input.value

    let resp = await fetch(`submit/${word1}/${word2}`)
    if (resp.ok) {
        let json = await resp.json()
        form.querySelector(".verdict").textContent = json.correct ? "Correct" : "Incorrect"
        if (json.correct) {
            form.querySelector(".correction").innerHTML = "&nbsp;"
        } else {
            form.querySelector(".correction").textContent = `The correct translation for '${word1} 'is '${json.pair.word2}'`
        }
    }

    nextWord(form)
}

async function nextWord(form) {
    let word1span = form.querySelector(".word1")
    let word2input = form.querySelector(".word2")

    resp = await fetch(`word`)
    if (resp.ok) {
        let json = await resp.json()
        word1span.textContent = json
        word2input.value = ""
    }
}

for (let form of document.querySelectorAll(".words")) {
    form.onsubmit = handleSubmit
    nextWord(form)
}
