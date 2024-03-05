// Use correct header image and set correct color

switch (location.hostname)
{
    case "mainframe.io":
        document.getElementById("img-logo-ktt").style.display = "none";
        document.getElementById("img-icon-lang").src = "/media/img/lang/icon.dark.svg";
        document.getElementsByTagName("html")[0].dataset["bsTheme"] = "dark";
        break;
    default:
        document.getElementById("img-logo-mainframe").style.display = "none";
        document.getElementById("img-icon-lang").src = "/media/img/lang/icon.light.svg";
        document.getElementsByTagName("html")[0].dataset["bsTheme"] = "light";
        break;
}
