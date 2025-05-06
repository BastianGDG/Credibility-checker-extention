chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "checkKilder",
    title: "🔍 Tjek Troværdighed",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "checkKilder" && info.selectionText) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const currentTab = tabs[0];
          if (currentTab && currentTab.url) {
              chrome.storage.local.set({ selectedText: info.selectionText, currentUrl: currentTab.url }, () => {
                  chrome.action.openPopup();
              });
          }
      });
  }
});