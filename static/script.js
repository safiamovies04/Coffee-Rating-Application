async function vote(id) {

    const response = await fetch("/vote", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: id
        })
    });

    const data = await response.json();

    document.getElementById("votes" + id).innerText = data.votes;
}