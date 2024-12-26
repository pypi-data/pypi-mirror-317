controlChannel.registerMessageHandler(ControlCommand.SERVER_PLAY, () => {
    getAudioElement().play();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_PAUSE, () => {
    getAudioElement().pause();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_PREVIOUS, () => {
    queue.previous();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_NEXT, () => {
    queue.next();
});

async function updateNowPlaying() {
    const audioElem = getAudioElement();
    const currentTrack = queue.currentTrack && queue.currentTrack.track ? queue.currentTrack.track : null;
    const duration = audioElem.duration ? audioElem.duration : (currentTrack ? queue.currentTrack.track.duration : null);
    if (duration) {
        await controlChannel.nowPlaying(currentTrack, audioElem.paused, audioElem.currentTime, duration);
    }
}

setInterval(updateNowPlaying, 30_000);

document.addEventListener('DOMContentLoaded', () => {
    const audioElem = getAudioElement();
    audioElem.addEventListener("play", updateNowPlaying);
    audioElem.addEventListener("pause", updateNowPlaying);
    audioElem.addEventListener("seeked", updateNowPlaying);
});
