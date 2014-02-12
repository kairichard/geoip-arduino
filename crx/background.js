var current_url = "";
var response = {}
function badge_ok(){
  chrome.browserAction.setBadgeText({text: "✓"});
  chrome.browserAction.setBadgeBackgroundColor({color:[0,255,0,255]});
}
function badge_waiting(){
  chrome.browserAction.setBadgeText({text: "<->"});
  chrome.browserAction.setBadgeBackgroundColor({color:[255,255,0,255]});
}
function badge_error(){
  chrome.browserAction.setBadgeText({text: "X"});
  chrome.browserAction.setBadgeBackgroundColor({color:[255,0,0,255]});
}
function init(){
  jQuery(document).ajaxError(badge_error).ajaxStart(badge_waiting).ajaxSuccess(badge_ok);
}

function handle(tab){
  if(tab.url == "newtab") return
  if(tab.url == "extensions") return
  jQuery.post("http://localhost:9000/locate", {url: tab.url}, function(data, status, xhr){
    response = data;
  });
}

(function(){
  init()
  jQuery.get("http://localhost:9000/connect")

  chrome.tabs.onUpdated.addListener(function(tabId, changeInfo) {
    if (changeInfo.status === 'complete') {
      chrome.tabs.get(tabId, function(tab){
        handle(tab)
      })
    }
  });
})()
