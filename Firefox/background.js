browser.runtime.onInstalled.addListener(() => {
  browser.contextMenus.create({
    id: "checkKilder",
    title: "🔍 Tjek Troværdighed",
    contexts: ["selection"]
  });
});

browser.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "checkKilder" && info.selectionText) {
    browser.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentTab = tabs[0];
      if (currentTab && currentTab.url) {
        browser.storage.local.set({ selectedText: info.selectionText, currentUrl: currentTab.url }, () => {
          browser.browserAction.openPopup();
        });
      }
    });
  }
});