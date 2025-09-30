/* =========================
   STATUS HANDLING
   ========================= */

const StatusApiUrl = "https://status.mainframe.io/api/statusStream?spaceOpen=1";
let statusSource = null;

/**
 * Remove prior context classes and apply Bootstrap 5.3 subtle variants.
 */
function applyContextClasses(el, context) {
    const contexts = ["primary", "secondary", "success", "danger", "warning", "info"];
    for (const c of contexts) {
        el.classList.remove(
            `bg-${c}-subtle`,
            `text-${c}-emphasis`,
            `border-${c}-subtle`,
            `btn-${c}`
        );
    }
    el.classList.add(`bg-${context}-subtle`, `text-${context}-emphasis`, `border-${context}-subtle`);
}

/**
 * Map raw state to a display state and Bootstrap context.
 */
function mapState(state) {
    switch (state) {
        case "none":
            return {display: "closed", context: "danger"};
        case "open":
        case "open+":
            return {display: "open", context: "success"};
        case "keyholder":
            return {display: "keyholder", context: "danger"};
        case "member":
            return {display: "member", context: "warning"};
        case "closing":
            return {display: "closing", context: "warning"};
        default:
            return {display: "unknown", context: "info"};
    }
}

/**
 * Ensure a status list item exists for the given room; create from template if needed.
 */
function ensureStatusItem(room) {
    let el = document.getElementById("status-" + room);
    if (el) return el;

    const tpl = document.getElementById("status-item-template");
    const parent = document.getElementById("space-status");
    if (!tpl || !parent) return null;

    el = tpl.content.firstElementChild.cloneNode(true);
    el.id = "status-" + room;

    parent.appendChild(el);
    return el;
}

/**
 * Apply a state to a room’s status item.
 */
function set_status(room, state) {
    const target = ensureStatusItem(room);
    if (!target) return;

    const {display, context} = mapState(state);

    const textBlocks = target.querySelectorAll(".status-text");
    textBlocks.forEach((n) => n.classList.toggle("d-none", n.dataset.state !== display));

    applyContextClasses(target, context);
}

/**
 * EventSource handlers
 */
function on_status_change(event) {
    const room = event.type;
    try {
        const payload = JSON.parse(event.data);
        set_status(room, payload.state);
    } catch (err) {
        console.error("Error while setting room status", room, err, event);
        set_status(room, "none");
    }
}

function init_status() {
    statusSource = new EventSource(StatusApiUrl);

    statusSource.onopen = function () {
        // connection ready
    };

    statusSource.onerror = function (err) {
        console.error("EventSource error.", err);
        try {
            statusSource.close();
        } catch {
        }
        statusSource = null;
        setTimeout(init_status, 5000);
    };

    statusSource.addEventListener("spaceOpen", on_status_change);
    statusSource.addEventListener("keepalive", function () {
    }, false);
}

init_status();

/* =========================
   CALENDAR
   ========================= */

const eventListElement = document.getElementById("event-list");
if (eventListElement) {

    const calendarConfig = {
        calendarId: eventListElement.dataset.calendarId,
        apiKey: eventListElement.dataset.apiKey,
        maxResults: Number(eventListElement.dataset.max || 5),
    };

    const dateFormatter = new Intl.DateTimeFormat("de-DE", {
        weekday: "short",
        day: "2-digit",
        month: "short",
    });
    const timeFormatter = new Intl.DateTimeFormat("de-DE", {
        hour: "2-digit",
        minute: "2-digit",
    });

    const parseDate = (value) => (value ? new Date(value) : null);

    const isSameDay = (a, b) =>
        a &&
        b &&
        a.getFullYear() === b.getFullYear() &&
        a.getMonth() === b.getMonth() &&
        a.getDate() === b.getDate();

    const inclusiveAllDayEnd = (endDateString) => new Date(new Date(endDateString).getTime() - 1);

    const cloneFromTemplate = (templateId) =>
        document.getElementById(templateId).content.firstElementChild.cloneNode(true);

    function formatDateLabel(googleEvent) {
        const startRaw = googleEvent.start.dateTime || googleEvent.start.date;
        const endRaw = googleEvent.end.dateTime || googleEvent.end.date;

        const start = parseDate(startRaw);
        const end = parseDate(endRaw);
        if (!start || !end) return "";

        const isAllDay = !!googleEvent.start.date && !!googleEvent.end.date;

        if (isAllDay) {
            return isSameDay(start, end)
                ? dateFormatter.format(start)
                : `${dateFormatter.format(start)} – ${dateFormatter.format(inclusiveAllDayEnd(endRaw))}`;
        }

        return isSameDay(start, end)
            ? dateFormatter.format(start)
            : `${dateFormatter.format(start)} – ${dateFormatter.format(end)}`;
    }

    function formatTimeLabel(googleEvent) {
        const startDT = googleEvent.start.dateTime;
        const endDT = googleEvent.end.dateTime;
        if (!startDT || !endDT) return ""; // no times for all-day events

        const start = new Date(startDT);
        const end = new Date(endDT);
        return `${timeFormatter.format(start)}–${timeFormatter.format(end)}`;
    }

    function renderEventList(items) {
        eventListElement.replaceChildren(); // clear

        if (!items || items.length === 0) {
            eventListElement.appendChild(cloneFromTemplate("event-empty-template"));
            return;
        }

        const itemTemplate = document.getElementById("event-item-template");
        const fragment = document.createDocumentFragment();

        items.slice(0, calendarConfig.maxResults).forEach((item) => {
            const listItem = itemTemplate.content.firstElementChild.cloneNode(true);

            const dateEl = listItem.querySelector(".event-date");
            const timeEl = listItem.querySelector(".event-time");
            const linkEl = listItem.querySelector(".event-link");

            const startIso = item.start.dateTime || item.start.date || "";
            dateEl.textContent = formatDateLabel(item);
            if (startIso) dateEl.setAttribute("datetime", startIso);

            const timeText = formatTimeLabel(item);
            timeEl.textContent = timeText;
            timeEl.classList.toggle("d-none", timeText === "");
            if (item.start.dateTime && timeText !== "") {
                timeEl.setAttribute("datetime", item.start.dateTime);
            } else {
                timeEl.removeAttribute("datetime");
            }

            linkEl.textContent = item.summary || "No Title";
            if (item.htmlLink) linkEl.href = item.htmlLink;

            fragment.appendChild(listItem);
        });

        eventListElement.appendChild(fragment);
    }

    function buildEventsUrl() {
        const nowIso = new Date().toISOString();
        const base = "https://www.mainframe.io/calendar/v3/calendars/";
        const id = encodeURIComponent(calendarConfig.calendarId);

        const params = new URLSearchParams({
            key: calendarConfig.apiKey,
            timeMin: nowIso,
            singleEvents: "true",
            orderBy: "startTime",
            maxResults: String(calendarConfig.maxResults),
        });

        return `${base}${id}/events?${params.toString()}`;
    }

    async function fetchEvents() {
        const response = await fetch(buildEventsUrl());
        const data = await response.json();
        return data.items || [];
    }

    (async () => {
        try {
            const events = await fetchEvents();
            renderEventList(events);
        } catch (err) {
            console.error("Error fetching Google Calendar events:", err);
            eventListElement.replaceChildren();
            eventListElement.appendChild(cloneFromTemplate("event-error-template"));
        }
    })();
} else {
    console.warn("#event-list not found; skipping calendar init");
}

/* =========================
   KEYBOARD + TOUCH HELPERS
   ========================= */

window.addEventListener("keydown", (e) => {
    let btn;
    switch (e.key) {
        case "ArrowLeft":
            btn = document.getElementById("album-image-previous");
            break;
        case "ArrowRight":
            btn = document.getElementById("album-image-next");
            break;
        case " ":
            btn = document.getElementById("img-controls-view");
            break;
        default:
            break;
    }

    if (btn) btn.click();
    return true;
});

const albumImageContainer = document.getElementById("album-image");
let startX = 0;
let endX = 0;

if (albumImageContainer) {
    albumImageContainer.addEventListener(
        "touchstart",
        function (e) {
            startX = e.touches[0].clientX;
        },
        false
    );

    albumImageContainer.addEventListener(
        "touchmove",
        function (e) {
            endX = e.touches[0].clientX;
        },
        false
    );

    albumImageContainer.addEventListener(
        "touchend",
        function () {
            const threshold = 50;

            if (startX && endX) {
                const diff = endX - startX;

                let btn;
                if (Math.abs(diff) > threshold) {
                    btn =
                        diff > 0
                            ? document.getElementById("album-image-previous")
                            : document.getElementById("album-image-next");
                }

                if (btn) btn.click();
            }

            startX = 0;
            endX = 0;
        },
        false
    );
}

/* =========================
   DEBUG API (global)
   ========================= */
/*
  Use in console:
  - StatusDebug.set('spaceOpen', 'open')
  - StatusDebug.random('spaceOpen')
  - StatusDebug.cycle('spaceOpen')
  - StatusDebug.send('spaceOpen', 'closing')  // goes through the same handler as EventSource
  - StatusDebug.pauseLive()
  - StatusDebug.resumeLive()
  - StatusDebug.clear('spaceOpen')
  - StatusDebug.help()
*/
(() => {
    const VALID_STATES = ["none", "open", "open+", "keyholder", "member", "closing"];
    const cycleIndexByRoom = new Map();

    function pauseLive() {
        if (statusSource) {
            try {
                statusSource.close();
            } catch {
            }
            statusSource = null;
            console.info("Status live stream paused.");
        } else {
            console.info("Status live stream is already paused.");
        }
    }

    function resumeLive() {
        if (!statusSource) {
            init_status();
            console.info("Status live stream resumed.");
        } else {
            console.info("Status live stream already running.");
        }
    }

    function send(room = "spaceOpen", state = "open") {
        const evt = {type: room, data: JSON.stringify({state})};
        on_status_change(evt);
    }

    function set(room = "spaceOpen", state = "open") {
        set_status(room, state);
    }

    function random(room = "spaceOpen") {
        const idx = Math.floor(Math.random() * VALID_STATES.length);
        const state = VALID_STATES[idx];
        set_status(room, state);
        return state;
    }

    function cycle(room = "spaceOpen") {
        const next = (cycleIndexByRoom.get(room) || 0) % VALID_STATES.length;
        const state = VALID_STATES[next];
        cycleIndexByRoom.set(room, next + 1);
        set_status(room, state);
        return state;
    }

    function clear(room = "spaceOpen") {
        const el = document.getElementById("status-" + room);
        if (el) {
            el.remove();
            console.info(`Removed status element for room "${room}".`);
        } else {
            console.info(`No status element found for room "${room}".`);
        }
    }

    function help() {
        console.table(
            [
                {cmd: "StatusDebug.set(room, state)", desc: "Set a specific room to a specific state."},
                {cmd: "StatusDebug.random(room)", desc: "Set room to a random valid state."},
                {cmd: "StatusDebug.cycle(room)", desc: "Cycle room through all valid states."},
                {cmd: "StatusDebug.send(room, state)", desc: "Simulate an EventSource message."},
                {cmd: "StatusDebug.pauseLive()", desc: "Pause the real EventSource stream."},
                {cmd: "StatusDebug.resumeLive()", desc: "Resume the real EventSource stream."},
                {cmd: "StatusDebug.clear(room)", desc: "Remove the rendered status element for a room."}
            ]
        );
        console.log("Valid states:", VALID_STATES.join(", "));
    }

    window.StatusDebug = {set, random, cycle, send, pauseLive, resumeLive, clear, help};
})();