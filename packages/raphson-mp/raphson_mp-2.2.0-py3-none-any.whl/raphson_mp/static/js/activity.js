function getNowPlayingCardHtml(info) {
    const card = document.createElement('div');
    card.classList.add('box');

    const cardHeader = document.createElement('div');
    cardHeader.classList.add('box-header');
    cardHeader.textContent = info.username;
    card.append(cardHeader);

    const cardBody = document.createElement('div');
    cardBody.classList.add('activity-box-body');
    card.append(cardBody);

    const coverThumbUrl = info.track ? `/track/${encodeURIComponent(info.track.path)}/cover?quality=low`: '/static/img/raphson_small.webp';
    const coverFullUrl = info.track ? `/track/${encodeURIComponent(info.track.path)}/cover?quality=high`: '/static/img/raphson.png';

    const coverImg = document.createElement('a');
    coverImg.classList.add('cover-img')
    coverImg.href = coverFullUrl;
    coverImg.style.backgroundImage = `url("${coverThumbUrl}")`;

    const imgInner = document.createElement('div');
    imgInner.classList.add('cover-img-overlay');

    if (info.paused) {
        imgInner.classList.add('icon-pause');
    }

    coverImg.append(imgInner);
    cardBody.append(coverImg);

    const infoDiv = document.createElement('div');
    cardBody.append(infoDiv);

    if (info.track && info.track.title && info.track.artists.length > 0) {
        const titleDiv = document.createElement('div');
        titleDiv.style.fontSize = '1.3em';
        titleDiv.textContent = info.track.title;
        const artistDiv = document.createElement('div');
        artistDiv.style.fontSize = '1.1em';
        artistDiv.textContent = info.track.artists.join(', ');
        infoDiv.append(titleDiv, artistDiv);
    } else {
        const fallbackDiv = document.createElement('div');
        fallbackDiv.style.fontSize = '1.1em';
        fallbackDiv.textContent = info.track ? info.track.display : "";
        infoDiv.append(fallbackDiv);
    }

    const playlistDiv = document.createElement('div');
    playlistDiv.classList.add('secondary');
    playlistDiv.textContent = info.track ? info.track.playlist : "";
    infoDiv.append(playlistDiv);

    const prevButton = createIconButton('skip-previous');
    prevButton.addEventListener('click', () => controlChannel.previous(info.player_id));
    infoDiv.append(" ", prevButton);

    if (info.paused) {
        const playButton = createIconButton('play');
        playButton.addEventListener('click', () => controlChannel.play(info.player_id));
        infoDiv.append(" ", playButton);
    } else {
        const pauseButton = createIconButton('pause');
        pauseButton.addEventListener('click', () => controlChannel.pause(info.player_id));
        infoDiv.append(" ", pauseButton);
    }

    const nextButton = createIconButton('skip-next');
    nextButton.addEventListener('click', () => controlChannel.next(info.player_id));
    infoDiv.append(" ", nextButton);

    const progressBar = document.createElement('div');
    progressBar.classList.add('activity-progress');
    progressBar.id = 'progress-' + info.player_id;
    progressBar.style.width = (100 * info.position / info.duration) + '%';
    card.append(progressBar);

    return card;
}

function createTableRow(contents) {
    const row = document.createElement('tr');
    for (const content of contents) {
        const col = document.createElement('td');
        col.textContent = content;
        row.append(col);
    }
    return row;
}

function getHistoryRowHtml(data) {
    return createTableRow([timestampToString(data.played_time), data.username, data.track.playlist, data.track.display]);
}

function getFileChangeRowHtml(data) {
    return createTableRow([timestampToString(data.change_time), data.username, data.action, data.track]);
}


document.addEventListener('DOMContentLoaded', async () => {
    const nowPlayingDiv = document.getElementById('now-playing');
    const nothingPlayingText = document.getElementById('nothing-playing-text');
    const historyTable = document.getElementById('tbody-history');
    const fileChangesTable = document.getElementById('tbody-changes');

    const nowPlayingData = {};

    controlChannel.registerMessageHandler(ControlCommand.SERVER_PLAYING, data => {
        nowPlayingData[data.player_id] = data;
        quickUpdate(true);
    });

    controlChannel.registerMessageHandler(ControlCommand.SERVER_PLAYED, data => {
        historyTable.prepend(getHistoryRowHtml(data));
        if (historyTable.childNodes.length > 10) {
            historyTable.childNodes[10].remove();
        }
    });

    controlChannel.registerMessageHandler(ControlCommand.SERVER_FILE_CHANGE, data => {
        fileChangesTable.prepend(getFileChangeRowHtml(data));
        if (fileChangesTable.childNodes.length > 10) {
            fileChangesTable.childNodes[10].remove();
        }
    });

    controlChannel.subscribe(ControlTopic.ACTIVITY);

    controlChannel.registerConnectHandler(() => {
        // when websocket connection is reopened, history entries are resent and exitisting ones must be removed
        historyTable.replaceChildren();
    });

    function quickUpdate(updateAll = false) {
        if (document.visibilityState != "visible") {
            return;
        }

        // Remove expired cards
        for (const now_playing of Object.values(nowPlayingData)) {
            if (Date.now() / 1000 - now_playing.update_time > 70) {
                delete nowPlayingData[now_playing.player_id];
                updateAll = true;
            }
        }

        nothingPlayingText.hidden = Object.keys(nowPlayingData).length > 0;

        if (updateAll) {
            nowPlayingDiv.replaceChildren(...Object.values(nowPlayingData).map(getNowPlayingCardHtml));
        }

        for (const now_playing of Object.values(nowPlayingData)) {
            if (now_playing.paused) {
                continue;
            }

            const corrected_position = now_playing.position + Date.now()/1000 - now_playing.update_time;
            if (corrected_position < 0 || corrected_position > now_playing.duration) {
                continue;
            }

            const progress = document.getElementById('progress-' + now_playing.player_id);
            if (!progress) {
                continue;
            }

            progress.style.width = (100 * corrected_position / now_playing.duration) + '%';
        }
    }

    setInterval(quickUpdate, 1000); /* interval must match progress transition in css */
    document.addEventListener("visibilitychange", quickUpdate);
});
