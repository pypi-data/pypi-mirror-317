document.addEventListener('DOMContentLoaded', () => {
    /** @type {HTMLButtonElement} */
    const syncButton = document.getElementById('sync-button');
    /** @type {HTMLButtonElement} */
    const stopButton = document.getElementById('stop-button');
    /** @type {HTMLTableElement} */
    const table = document.getElementById('table');
    /** @type {HTMLTableSectionElement} */
    const log = document.getElementById('log');
    /** @type {HTMLParagraphElement} */
    const wait = document.getElementById('wait');

    const decoder = new TextDecoder();

    function createRow(entry) {
        const tdTask = document.createElement('td');
        tdTask.textContent = entry.task;
        const tdIcon = document.createElement('td');
        if (entry.done) {
            tdIcon.classList.add('icon', 'icon-check', 'icon-col');
        } else {
            tdIcon.classList.add('icon', 'icon-loading', 'spinning', 'icon-col');
        }
        const row = document.createElement('tr');
        row.dataset.task = entry.task;
        row.append(tdTask, tdIcon);
        return row
    }

    function handleEntry(entry) {
        console.debug('received value', entry);

        if (entry == "stopped") {
            syncButton.hidden = false;
            stopButton.hidden = true;
            wait.hidden = true;
            return;
        } else if (entry == "running") {
            syncButton.hidden = true;
            stopButton.hidden = false;
            return;
        }

        table.hidden = false;
        wait.hidden = true;

        entry = JSON.parse(entry);
        if (entry.done) {
            if (entry.task == "stop") {
                // All done, any loading icons should be replaced by stop icon
                for (const elem of document.querySelectorAll('.icon-loading')) {
                    elem.classList.remove('icon-loading', 'spinning');
                    elem.classList.add('icon-close');
                }
            } else {
                // Task done
                for (const row of log.children) {
                    if (row.dataset.task == entry.task) {
                        row.replaceWith(createRow(entry));
                    }
                }
            }
        } else {
            // Task start
            log.append(createRow(entry));
        }

        if (log.children.length > 20) {
            log.children[0].remove();
        }
    }

    async function handleResponse(result) {
        const values = decoder.decode(result.value);
        for (const value of values.split('\n')) {
            if (value) {
                handleEntry(value)
            }
        }
        return result
    }

    syncButton.addEventListener('click', async () => {
        const response = await fetch('/offline/start', {method: 'POST'});
        checkResponseCode(response);
    });

    stopButton.addEventListener('click', async () => {
        const response = await fetch('/offline/stop', {method: 'POST'});
        checkResponseCode(response);
    });

    async function monitor() {
        try {
            const response = await fetch('/offline/monitor', {method: 'GET'});
            checkResponseCode(response);
            const reader = response.body.getReader();

            async function process() {
                result = await reader.read();
                if (result.done) {
                    return reader.closed;
                }
                await handleResponse(result);
                await process();
            }

            await process();
        } catch (err) {
            console.error(err);
        } finally {
            wait.hidden = false; // status is not known
        }

        setTimeout(monitor, 1000);
    }

    monitor();
});
