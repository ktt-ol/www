/* =========================
   PCB BACKGROUND
   ========================= */

// PCB Background Configuration
const PCB_CONFIG = {
    useRandomGeneration: true,  // Set to false to use only fixed traces
    randomTraceCount: {min: 5, max: 15},  // Number of random traces when useRandomGeneration is true
    gridSize: 32,  // Grid cell size in pixels
};

// PCB Background (Non-interactive)
class PCBCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');

        // Grid system for alignment
        this.gridSize = PCB_CONFIG.gridSize;

        this.init();
    }

    init() {
        this.resizeCanvas();
        this.drawBackground();
        this.setupEventListeners();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    snapToGrid(value) {
        return Math.round(value / this.gridSize) * this.gridSize;
    }

    drawBackground() {
        // Dark background (#222222)
        this.ctx.fillStyle = '#222222';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Add decorative PCB traces in the background (no visible grid)
        this.drawDecorativeTraces();
    }

    drawDecorativeTraces() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Calculate grid dimensions
        const gridCols = Math.floor(w / this.gridSize);
        const gridRows = Math.floor(h / this.gridSize);

        // Track occupied grid cells to prevent overlaps
        const occupiedCells = new Set();

        // Store all traces
        const traces = [];

        // Draw multiple decorative traces with branching
        this.ctx.strokeStyle = 'rgba(0, 160, 255, 0.06)';
        this.ctx.lineWidth = 2;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';

        // Add fixed traces first
        this.addFixedTraces(gridCols, gridRows, occupiedCells, traces);

        // Add random traces if enabled
        if (PCB_CONFIG.useRandomGeneration) {
            const numRandomTraces = Math.floor(
                Math.random() * (PCB_CONFIG.randomTraceCount.max - PCB_CONFIG.randomTraceCount.min + 1)
            ) + PCB_CONFIG.randomTraceCount.min;

            for (let i = 0; i < numRandomTraces; i++) {
                // Generate a horizontal trace that starts from left or right edge
                const trace = this.generateGridBasedTrace(gridCols, gridRows, occupiedCells);
                if (trace) {
                    traces.push(trace);
                    this.drawDecorativeTrace(trace);
                }
            }
        }
    }

    addFixedTraces(gridCols, gridRows, occupiedCells, traces) {
        // Fixed trace patterns that always appear
        const fixedTraceConfigs = [
            // Trace 1: Top left to mid right
            {
                startCol: 0,
                startRow: Math.floor(gridRows * 0.2),
                direction: 1,
                segments: [
                    {type: 'h', length: Math.floor(gridCols * 0.6)},
                    {type: 'v', length: Math.floor(gridRows * 0.15)},
                    {type: 'h', length: Math.floor(gridCols * 0.2)}
                ]
            },
            // Trace 2: Top right to mid left
            {
                startCol: gridCols - 1,
                startRow: Math.floor(gridRows * 0.35),
                direction: -1,
                segments: [
                    {type: 'h', length: Math.floor(gridCols * 0.5)},
                    {type: 'v', length: -Math.floor(gridRows * 0.1)},
                    {type: 'h', length: Math.floor(gridCols * 0.25)}
                ]
            },
            // Trace 3: Bottom left to mid right
            {
                startCol: 0,
                startRow: Math.floor(gridRows * 0.7),
                direction: 1,
                segments: [
                    {type: 'h', length: Math.floor(gridCols * 0.65)},
                    {type: 'v', length: Math.floor(gridRows * 0.1)},
                    {type: 'h', length: Math.floor(gridCols * 0.15)}
                ]
            },
            // Trace 4: Bottom right to center
            {
                startCol: gridCols - 1,
                startRow: Math.floor(gridRows * 0.8),
                direction: -1,
                segments: [
                    {type: 'h', length: Math.floor(gridCols * 0.55)},
                    {type: 'v', length: -Math.floor(gridRows * 0.12)},
                    {type: 'h', length: Math.floor(gridCols * 0.2)}
                ]
            }
        ];

        for (const config of fixedTraceConfigs) {
            const trace = this.generateFixedTrace(config, gridCols, gridRows, occupiedCells);
            if (trace) {
                traces.push(trace);
                this.drawDecorativeTrace(trace);
            }
        }
    }

    generateFixedTrace(config, gridCols, gridRows, occupiedCells) {
        const path = [{col: config.startCol, row: config.startRow}];
        let currentCol = config.startCol;
        let currentRow = config.startRow;

        // Mark starting cell
        occupiedCells.add(`${currentCol},${currentRow}`);

        for (const segment of config.segments) {
            if (segment.type === 'h') {
                // Horizontal movement
                const direction = segment.length > 0 ? 1 : -1;
                const absLength = Math.abs(segment.length);

                for (let i = 0; i < absLength; i++) {
                    const newCol = currentCol + direction;
                    if (newCol < 0 || newCol >= gridCols) break;

                    const cellKey = `${newCol},${currentRow}`;
                    if (occupiedCells.has(cellKey)) break;

                    currentCol = newCol;
                    path.push({col: currentCol, row: currentRow});
                    occupiedCells.add(cellKey);
                }
            } else if (segment.type === 'v') {
                // Vertical movement
                const direction = segment.length > 0 ? 1 : -1;
                const absLength = Math.abs(segment.length);

                for (let i = 0; i < absLength; i++) {
                    const newRow = currentRow + direction;
                    if (newRow < 0 || newRow >= gridRows) break;

                    const cellKey = `${currentCol},${newRow}`;
                    if (occupiedCells.has(cellKey)) break;

                    currentRow = newRow;
                    path.push({col: currentCol, row: currentRow});
                    occupiedCells.add(cellKey);
                }
            }
        }

        return path.length > 1 ? {main: path, branches: []} : null;
    }

    generateGridBasedTrace(gridCols, gridRows, occupiedCells) {
        // Start from left or right edge
        const fromLeft = Math.random() > 0.5;
        const startCol = fromLeft ? 0 : gridCols - 1;

        // Pick a Y position (grid row) that doesn't conflict
        let startRow;
        let attempts = 0;
        const maxAttempts = 50;

        do {
            startRow = Math.floor(Math.random() * (gridRows - 2)) + 1; // Avoid top and bottom edges
            attempts++;

            // Check if this row is available (not occupied)
            const cellKey = `${startCol},${startRow}`;
            if (!occupiedCells.has(cellKey)) {
                break;
            }
        } while (attempts < maxAttempts);

        if (attempts >= maxAttempts) {
            return null; // Couldn't find a good spot
        }

        // Generate main trace path on the grid
        const mainTrace = this.generateGridPath(startCol, startRow, gridCols, gridRows, fromLeft, occupiedCells);

        if (!mainTrace || mainTrace.length < 2) {
            return null;
        }

        // 30% chance to add 1 branch
        const branches = [];
        if (Math.random() > 0.7 && mainTrace.length > 3) {
            const branchIndex = Math.floor(Math.random() * (mainTrace.length - 2)) + 1;
            const branchPoint = mainTrace[branchIndex];
            const branchPath = this.generateGridBranch(
                branchPoint.col,
                branchPoint.row,
                gridCols,
                gridRows,
                fromLeft,
                occupiedCells
            );
            if (branchPath && branchPath.length > 1) {
                branches.push({start: branchIndex, path: branchPath});
            }
        }

        return {main: mainTrace, branches: branches};
    }

    generateGridPath(startCol, startRow, gridCols, gridRows, fromLeft, occupiedCells) {
        const path = [{col: startCol, row: startRow}];

        // Mark starting cell as occupied
        occupiedCells.add(`${startCol},${startRow}`);

        let currentCol = startCol;
        let currentRow = startRow;

        // Determine how far to traverse (70-100% of width) - increased for longer traces
        const targetColDistance = Math.floor((gridCols - 2) * (0.7 + Math.random() * 0.3));
        let colsTraveled = 0;

        // Number of segments (2-4 turns)
        const numSegments = Math.floor(Math.random() * 3) + 2;

        for (let i = 0; i < numSegments && colsTraveled < targetColDistance; i++) {
            if (i % 2 === 0) {
                // Move horizontally
                const direction = fromLeft ? 1 : -1;
                const segmentLength = Math.floor(Math.random() * 10) + 6; // 6-15 grid cells (increased for longer traces)

                for (let step = 0; step < segmentLength && colsTraveled < targetColDistance; step++) {
                    const newCol = currentCol + direction;

                    // Check bounds
                    if (newCol < 0 || newCol >= gridCols) break;

                    // Check if cell is occupied
                    const cellKey = `${newCol},${currentRow}`;
                    if (occupiedCells.has(cellKey)) break;

                    currentCol = newCol;
                    colsTraveled++;
                    path.push({col: currentCol, row: currentRow});
                    occupiedCells.add(cellKey);
                }
            } else {
                // Move vertically (smaller movements)
                const verticalMove = Math.floor(Math.random() * 5) - 2; // -2 to +2 grid cells
                const newRow = Math.max(1, Math.min(gridRows - 2, currentRow + verticalMove));

                if (newRow !== currentRow) {
                    const direction = newRow > currentRow ? 1 : -1;

                    // Move one cell at a time vertically
                    while (currentRow !== newRow) {
                        currentRow += direction;
                        const cellKey = `${currentCol},${currentRow}`;

                        if (occupiedCells.has(cellKey)) {
                            currentRow -= direction; // Step back
                            break;
                        }

                        path.push({col: currentCol, row: currentRow});
                        occupiedCells.add(cellKey);
                    }
                }
            }
        }

        return path;
    }

    generateGridBranch(startCol, startRow, gridCols, gridRows, fromLeft, occupiedCells) {
        const path = [{col: startCol, row: startRow}];

        let currentCol = startCol;
        let currentRow = startRow;

        // Branches are shorter (2-3 segments)
        const numSegments = Math.floor(Math.random() * 2) + 2;

        for (let i = 0; i < numSegments; i++) {
            const segmentLength = Math.floor(Math.random() * 4) + 2; // 2-5 grid cells

            if (i % 2 === 0) {
                // Move vertically or horizontally perpendicular
                if (Math.random() > 0.5) {
                    // Vertical
                    const direction = Math.random() > 0.5 ? 1 : -1;
                    for (let step = 0; step < segmentLength; step++) {
                        const newRow = currentRow + direction;
                        if (newRow < 1 || newRow >= gridRows - 1) break;

                        const cellKey = `${currentCol},${newRow}`;
                        if (occupiedCells.has(cellKey)) break;

                        currentRow = newRow;
                        path.push({col: currentCol, row: currentRow});
                        occupiedCells.add(cellKey);
                    }
                } else {
                    // Horizontal
                    const direction = fromLeft ? 1 : -1;
                    for (let step = 0; step < segmentLength; step++) {
                        const newCol = currentCol + direction;
                        if (newCol < 0 || newCol >= gridCols) break;

                        const cellKey = `${newCol},${currentRow}`;
                        if (occupiedCells.has(cellKey)) break;

                        currentCol = newCol;
                        path.push({col: currentCol, row: currentRow});
                        occupiedCells.add(cellKey);
                    }
                }
            } else {
                // Alternate direction
                const direction = fromLeft ? 1 : -1;
                for (let step = 0; step < segmentLength; step++) {
                    const newCol = currentCol + direction;
                    if (newCol < 0 || newCol >= gridCols) break;

                    const cellKey = `${newCol},${currentRow}`;
                    if (occupiedCells.has(cellKey)) break;

                    currentCol = newCol;
                    path.push({col: currentCol, row: currentRow});
                    occupiedCells.add(cellKey);
                }
            }
        }

        return path;
    }

    drawDecorativeTrace(trace) {
        // Convert grid coordinates to pixel coordinates
        const mainPath = trace.main.map(point => ({
            x: point.col * this.gridSize,
            y: point.row * this.gridSize
        }));

        // Draw main trace
        this.ctx.strokeStyle = 'rgba(0, 160, 255, 0.06)';
        this.ctx.beginPath();
        this.ctx.moveTo(mainPath[0].x, mainPath[0].y);
        for (let i = 1; i < mainPath.length; i++) {
            this.ctx.lineTo(mainPath[i].x, mainPath[i].y);
        }
        this.ctx.stroke();

        // Draw vias at grid intersections (all points are on grid intersections)
        this.ctx.fillStyle = 'rgba(0, 160, 255, 0.08)';
        for (let i = 0; i < mainPath.length; i++) {
            // Draw via only at endpoints and every 6th point (reduced via count)
            if (i === 0 || i === mainPath.length - 1 || (i % 6 === 0 && i > 0)) {
                this.drawVia(mainPath[i].x, mainPath[i].y);
            }
        }

        // Draw branches
        for (const branch of trace.branches) {
            const branchPath = branch.path.map(point => ({
                x: point.col * this.gridSize,
                y: point.row * this.gridSize
            }));

            this.ctx.strokeStyle = 'rgba(0, 160, 255, 0.06)';
            this.ctx.beginPath();
            this.ctx.moveTo(branchPath[0].x, branchPath[0].y);
            for (let i = 1; i < branchPath.length; i++) {
                this.ctx.lineTo(branchPath[i].x, branchPath[i].y);
            }
            this.ctx.stroke();

            // Draw via at branch connection point and endpoint
            this.drawVia(branchPath[0].x, branchPath[0].y);
            this.drawVia(branchPath[branchPath.length - 1].x, branchPath[branchPath.length - 1].y);
        }
    }

    drawVia(x, y) {
        // Draw a via (small circle with ring) at exact grid position
        this.ctx.fillStyle = 'rgba(0, 160, 255, 0.08)';
        this.ctx.beginPath();
        this.ctx.arc(x, y, 4, 0, Math.PI * 2);
        this.ctx.fill();

        // Inner darker circle
        this.ctx.fillStyle = '#222222';
        this.ctx.beginPath();
        this.ctx.arc(x, y, 2, 0, Math.PI * 2);
        this.ctx.fill();
    }

    setupEventListeners() {
        // Handle window resize - just redraw the background
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.drawBackground();
        });
    }
}

// Initialize PCB background when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('pcbCanvas');
    if (canvas) {
        new PCBCanvas('pcbCanvas');
    }
});

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
 * Apply a state to a room's status item.
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

/* =========================
   PCB DEBUG API (global)
   ========================= */
/*
  Use in console:
  - PCBDebug.setRandomGeneration(true/false)  // Enable/disable random trace generation
  - PCBDebug.setRandomCount(min, max)  // Set range for random trace count
  - PCBDebug.getConfig()  // View current configuration
  - PCBDebug.redraw()  // Redraw the background with current settings
  - PCBDebug.help()
*/
(() => {
    let pcbCanvasInstance = null;

    // Store reference when PCBCanvas is created
    const originalDOMContentLoaded = document.addEventListener;

    function setRandomGeneration(enabled) {
        PCB_CONFIG.useRandomGeneration = enabled;
        console.info(`Random trace generation ${enabled ? 'enabled' : 'disabled'}. Call PCBDebug.redraw() to apply.`);
    }

    function setRandomCount(min, max) {
        if (min < 0 || max < min) {
            console.error("Invalid range. Min must be >= 0 and max must be >= min.");
            return;
        }
        PCB_CONFIG.randomTraceCount.min = min;
        PCB_CONFIG.randomTraceCount.max = max;
        console.info(`Random trace count set to ${min}-${max}. Call PCBDebug.redraw() to apply.`);
    }

    function getConfig() {
        console.table({
            "Random Generation": PCB_CONFIG.useRandomGeneration,
            "Random Count (min)": PCB_CONFIG.randomTraceCount.min,
            "Random Count (max)": PCB_CONFIG.randomTraceCount.max,
            "Grid Size": PCB_CONFIG.gridSize
        });
        return PCB_CONFIG;
    }

    function redraw() {
        const canvas = document.getElementById('pcbCanvas');
        if (canvas) {
            // Create new instance which will redraw
            new PCBCanvas('pcbCanvas');
            console.info("PCB background redrawn with current configuration.");
        } else {
            console.warn("PCB canvas element not found.");
        }
    }

    function help() {
        console.table([
            {cmd: "PCBDebug.setRandomGeneration(true/false)", desc: "Enable or disable random trace generation"},
            {cmd: "PCBDebug.setRandomCount(min, max)", desc: "Set range for random trace count (e.g., 5, 15)"},
            {cmd: "PCBDebug.getConfig()", desc: "View current PCB configuration"},
            {cmd: "PCBDebug.redraw()", desc: "Redraw background with current settings"}
        ]);
        console.log("Current config:", PCB_CONFIG);
    }

    window.PCBDebug = {setRandomGeneration, setRandomCount, getConfig, redraw, help};
})();
