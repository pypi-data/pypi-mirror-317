(script) => {
    window.rw_play_result = undefined;
    var player = new jsReplay.playback(script, (result) => {window.rw_play_result = result;})
    player.start();
}