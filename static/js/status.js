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
 * @param {string} room_name
 * @param {string} color
 */
function set_button_color(room_name, color) {
    let id = States.button_id_prefix + room_name;
    for (let state of States.all_states) {
        document.getElementById(id).classList.remove(state.color);
    }
    document.getElementById(id).classList.add(color);
}

/**
 * @param {string} room_name
 * @param {string} state_name
 */
function set_room_status(room_name, state_name) {
    let state = States.state_map[state_name];
    if (state) {
        let room = Rooms.find(r => r.name === room_name);

        if (room) {
            for (let status of States.all_states) {
                document.getElementById(`${States.text_id_prefix + status.name}-${room.name}`).classList.add("d-none");
            }
            document.getElementById(`${States.text_id_prefix + state.name}-${room.name}`).classList.remove("d-none");
            set_button_color(room_name, state.color)
        } else {
            throw new Error(`Unknown room supplied: ${room_name}`)
        }
    } else {
        set_room_status(room_name, "unknown");
        throw new Error(`Unknown status option supplied: ${state_name}`)
    }
}

async function fetch_current_status() {
    let currentStatus = await (await fetch(ApiUrl)).json();
    console.info("Processing current status information", currentStatus);

    for (let room_name in currentStatus) {
        try {
            set_room_status(room_name, currentStatus[room_name].state);
        } catch (error) {
            console.error("An error occurred:", error)
        }
    }
}

function set_all_rooms(state_name = "closed") {
    if (!States.state_map[status]) {
        throw new Error(`Unknown status option supplied: ${state_name}`)
    }

    for (let room of Rooms) {
        set_room_status(room.name, state_name);
    }
}

fetch_current_status();
setInterval(fetch_current_status, 5000);