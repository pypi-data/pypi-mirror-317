import sys
import playwright
from pathlib import Path


__dir__ = Path(__file__).parent
__version__ = "1.0.0"


def install(page, path=".", output=sys.stderr):
    """
    Installs the Recordwright javascript sources in a page.
    
    Args:
        page (Page): The playwright page the Recordwright sources should be inject.
        path (str): Directory location, where to save and load the recordings.
        output (file): output stream for messages. (Default sys.stderr)

    Returns:
        RecorderPlayer: Interface for recording and replaying interactions.
    """
    return RecorderPlayer(page, path, output).inject()


class RecorderPlayer:
    """
    Records Interactions and replays them
    """

    def __init__(self, page, path=".", output=sys.stderr):
        self.page = page
        self.path = Path(path).absolute()
        self.output = output
        self.page.on("load", self.inject)

    def inject(self):
        if self.page.evaluate("() => { if (! window.$) { return 1;} else {return 0;}}"):
            jquery = __dir__ / "jquery-3.7.0.min.js"
            self.page.evaluate(jquery.read_text())

        dndsim = __dir__ / "dndsim.js"
        self.page.evaluate(dndsim.read_text())

        replay = __dir__ / "replay.js"
        self.page.evaluate(replay.read_text())
        return self
        

    def interaction(self, name, description=None):
        """
        Records or replays a interaction. If a replay file exists it will be replayed,
        otherwise a replay file will be created by recording an interaction.

        Args:
            name (str): Name of the interaction
            description (str): Description of the interaction, 
                that is shown while recording.
        """

        if not name.endswith(".json"):
            name += ".json"

        path = self.path / name

        while True:
            if not path.exists():
                print("-------------------"+"-"*len(name), file=self.output)
                print("record interaction", name, file=self.output)
                if description:
                    print(description, file=self.output)
                print("stop with ctrl+shift+f11", file=self.output)
                
                self.page.evaluate(self._get_recorder())
                self.page.wait_for_function("() => window.rw_record_script !== undefined", timeout=120000)
                script = self.page.evaluate("() => window.rw_record_script")
                path.write_text(script)
                print("recording done", file=self.output)
                break
            else:
                print("play", name, file=self.output)
                self.page.evaluate(self._get_player(), path.read_text())

                self.page.wait_for_function("() => window.rw_play_result !== undefined", timeout=200000)
                result = self.page.evaluate("() => window.rw_play_result")

                if result is True:
                    print("done", file=self.output)
                    break
                else:
                    print("Error Playback", name, file=self.output)
                    print(result, file=self.output)
                    print("Rerecord? Y(es)/N(o)", file=self.output)
                    answer = input().strip()
                    if answer.lower() == "y":
                        path.unlink()
                    else:
                        raise RuntimeError("Error Playback", result)
                        
    def _get_recorder(self):
        try:
            return self._recorder
        except AttributeError:
            js = __dir__ / "record.js"
            self._recorder = js.read_text()
        return self._recorder

    def _get_player(self):
            try:
                return self._player
            except AttributeError:
                js = __dir__ / "play.js"
                self._player = js.read_text()
            return self._player
