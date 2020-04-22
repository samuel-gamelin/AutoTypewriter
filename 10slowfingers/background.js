var urlRegex = new RegExp(".:\/\/*.(10ff.net|10fastfingers.com).*")

/**
 * Handles the action when the extension icon is clicked.
 */
chrome.browserAction.onClicked.addListener(function (tab) {
    if (urlRegex.test(tab.url)) {
        chrome.tabs.sendMessage(tab.id, { msg: 'submit' }, () => console.log("Got a response"));
    } else {
        alert("You can only use this on the 10fastfingers.com or 10ff.net website.");
    }
});
