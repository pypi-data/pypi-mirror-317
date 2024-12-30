() => {
    var stoprecord = (event) => {
        if (event.key == "F11" && event.ctrlKey && event.shiftKey) {
            script = jsReplay.record.stop()
            event.preventDefault();
            window.removeEventListener("keydown", stoprecord, {capture: true});
            console.log("script", script);
            window.rw_record_script = script;        
        }
    }
    window.rw_record_script = undefined;
    window.addEventListener("keydown", stoprecord, {capture: true});
    jsReplay.record.start();
}