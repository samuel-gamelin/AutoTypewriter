chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.msg && (request.msg === "submit")) {
        let response = "";

        if (document.getElementById("row1")) { // Singleplayer on 10fastfingers.com
            [...document.getElementById("row1").childNodes].forEach(element => {
                if (element.innerText) {
                    response += element.innerText + " ";
                }
            });
        } else if (document.querySelectorAll(".place")[0]) { // Multiplayer on 10ff.net
            [...document.querySelectorAll(".place")[0].childNodes].forEach(element => {
                if (element.innerText) {
                    response += element.innerText + " ";
                } else {
                    response += " ";
                }
            });
        } else {
            console.warn("Could not find any words");
            sendResponse();
            return;
        }

        chrome.storage.local.get(["access_token"], (items) => {
            let access_token;
            if (Object.keys(items).length === 0) {
                access_token = prompt("You don't have a paste.ee API token set yet. Please enter one below.");
                chrome.storage.local.set({ "access_token": access_token }, function () {
                    console.log("Access token set!");
                });
            } else {
                access_token = items["access_token"];
            }
            const url = "https://api.paste.ee/v1/pastes";
            fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': access_token
                },
                body: JSON.stringify({
                    desciption: "Test",
                    sections: [
                        {
                            name: "section1",
                            contents: response
                        }
                    ]
                })
            })
                .then(response => response.json())
                .then(result => {
                    console.log("Success! Paste URL: " + result['link']);
                })
                .catch(() => {
                    console.warn("Error submitting paste. Please try again.");
                })
        });
        sendResponse();
    }
});
