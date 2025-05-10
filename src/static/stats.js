function createStatsEntry(pair) {
    let stats = document.createElement("stats")
    let score = document.createElement("stats-score")
    score.innerText = pair.score.toLocaleString(undefined, { style: "percent", maximumFractionDigits: 0 })
    let correct = document.createElement("stats-correct")
    let incorrect = document.createElement("stats-incorrect")
    correct.innerText = pair.correct
    incorrect.innerText = pair.incorrect
    stats.appendChild(score)
    stats.appendChild(correct)
    stats.appendChild(incorrect)
    let word1 = document.createElement("word1")
    let word2 = document.createElement("word2")
    word1.innerText = pair.word1
    word2.innerText = pair.word2
    let wordPair = document.createElement("wordpair")
    wordPair.appendChild(stats)
    wordPair.append(word1)
    wordPair.append(word2)
    return wordPair
}

async function loadStats(container) {
    let resp = await fetch(`stats-api`)
    if (resp.ok) {
        let json = await resp.json()
        for (let pair of json.pairs) {
            container.appendChild(createStatsEntry(pair))
        }
    } else {
        console.log(resp)
    }
}

for (let container of document.querySelectorAll("unit-stats")) {
    loadStats(container)
}
