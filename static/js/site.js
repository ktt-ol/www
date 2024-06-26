function isDarkModeEnabled() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

if (isDarkModeEnabled()) {
    document.getElementsByTagName("html")[0].dataset["bsTheme"] = "dark";
    document.getElementById("img-icon-lang").src = "/media/img/lang/icon.dark.svg";
} else {

    document.getElementsByTagName("html")[0].dataset["bsTheme"] = "light";
    document.getElementById("img-icon-lang").src = "/media/img/lang/icon.light.svg";
}

switch (location.hostname) {
    case "mainframe.io":
        document.getElementById("img-logo-mainframe").style.display = "inline";
        document.getElementById("img-logo-ktt").style.display = "none";
        break;
    default:
        document.getElementById("img-logo-mainframe").style.display = "none";
        document.getElementById("img-logo-ktt").style.display = "inline";
        break;
}
