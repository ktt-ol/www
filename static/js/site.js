/*
    mainframe / ktt-ol theme switch
 */

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


/*
   status handling
*/

const ApiUrl = "https://status.kreativitaet-trifft-technik.de/api/openState";

const StateClosed = {
    name: "closed",
    color: "btn-danger"
};

const StateClosing = {
    name: "closing",
    color: "btn-warning"
};

const StateOpen = {
    name: "open",
    color: "btn-success"
};

const StateUnknown = {
    name: "unknown",
    color: "btn-info"
};

const States = {
    text_id_prefix: "status-text-",
    button_id_prefix: "status-",
    all_states: [
        StateClosed,
        StateClosing,
        StateOpen,
        StateUnknown
    ],
    state_map: {
        "none": StateClosed,
        "closing": StateClosing,
        "open": StateOpen,
        "open+": StateOpen,
        "unknown": StateUnknown
    },
};

/**
 * @param {string} id
 * @param {string} color
 */
function set_button_color(id, color) {
    for (let state of States.all_states) {
        document.getElementById(id).classList.remove(state.color);
    }
    document.getElementById(id).classList.add(color);
}

/**
 * @param {string} room_name
 * @param {string} state_name
 * @param {string} id
 */
function set_room_status(room_name, state_name, id) {
    let state = States.state_map[state_name];
    if (state) {
        let room = Rooms.find(r => r.name === room_name);

        if (room) {
            for (let status of States.all_states) {
                document.getElementById(`${States.text_id_prefix + status.name}-${room.name}`).classList.add("d-none");
            }
            document.getElementById(`${States.text_id_prefix + state.name}-${room.name}`).classList.remove("d-none");
            set_button_color(id, state.color);

            return true;
        } else {
            throw new Error(`Unknown room supplied: ${room_name}`);
        }
    } else {
        set_room_status(room_name, "unknown", id);
        throw new Error(`Unknown status option supplied: ${state_name}`);
    }
}

async function fetch_current_status() {
    let currentStatus = await (await fetch(ApiUrl)).json();
    console.info("Processing current status information", currentStatus);

    let status_buttons = [];
    let status_button_elements = document.getElementById("space-status").children;
    for (let room of status_button_elements) {
        status_buttons.push(room.getAttribute("id"));
    }

    for (let room_name in currentStatus) {
        try {
            let id = States.button_id_prefix + room_name;
            set_room_status(room_name, currentStatus[room_name].state, id);
            status_buttons.splice(status_buttons.indexOf(id), 1);
        } catch (error) {
            console.error("An error occurred:", error);
        }
    }

    for (let room_name of status_buttons) {
        set_button_color(room_name, StateUnknown.color);
    }
}

function set_all_rooms(state_name = "closed") {
    if (!States.state_map[status]) {
        throw new Error(`Unknown status option supplied: ${state_name}`);
    }

    for (let room of Rooms) {
        set_room_status(room.name, state_name, id);
    }
}

fetch_current_status().then();
setInterval(fetch_current_status, 60000);