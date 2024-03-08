const ifsImageCount = 5;
var currentIfsImage = 0;
function isDarkModeEnabled() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

function nextIfsImage(direction)
{
    currentIfsImage += direction;
    currentIfsImage = Math.abs(currentIfsImage % ifsImageCount);

    for(let i = 0; i < ifsImageCount; i++)
    {
        let element = document.getElementById("ifs-image-" + i);
        if(i === currentIfsImage)
        {
            element.classList.remove("d-none");
        } else {
            if(!element.classList.contains("d-none"))
            {
                element.classList.add("d-none")
            }
        }
    }
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
