/*
 *   jsReplay (v0.0.1)
 *   https://github.com/elliotnb/js-replay
 *
 *   Licensed under the MIT license:
 *   http://www.opensource.org/licenses/MIT
 *
 *  jsReplay is a record and playback tool used for functional regression testing. It is a singleton with two modes of operation: record and playback.
 *
 *  In record mode, jsReplay will record all user events that occur on the page and log them silently in the background. When the recording is stopped,
 *  the entire user event log is sent to the console in JSON format.
 *
 *  In playback mode, jsReplay will read in a previously recorded JSON file, simulate all the user events and log any errors or mismatched elements on the page.
 *  When playback stops, a log of discrepancies and/or errors that occured during the playback is sent to the console in JSON format.
 *
 *  Playback usage:
 *
 *    To playback a regression test you must first instantiate a new playback object. The constructor accepts two arguments
 *    - a string with the playback script
 *    - a callback that is invoked after the playback has finished.
 *    The playback will not start until the start() method is invoked. Only one playback instance can run at a time.
 *
 *    var widgetTest = new jsReplay.playback(script, finished_callbach);
 *    widgetTest.start();
 *
 *  Record usage:
 *
 *    To record a regression test, execute the following command:
 *
 *    jsReplay.record.start();
 *
 *    When you've finished recording your regression test, execute the following command:
 *
 *    jsReplay.record.stop();
 *
 *    The test script is returned by stop
 *

Modifications for recordwright:

  - The testscript is returned by record.stop()
  - jsReplay.playback  accepts a testscript and a finished callback function
  - Fixes for playing
  - Additional Events: contextmenu, dblclick, dragdrop

 */
  var jsReplay = (function() {

    // Indicates whether or not jsReplay is playing back user events. When set to true, jsReplay will not start another playback nor record user events.
    var playbackInProgress = false;
  
    // Indicates whether or not jsReplay is recording user events. When set to true, jsReplay will not start another recording nor start a playback.
    var recordInProgress = false;
  
    return {
  
      "playback": (function() {
  
          var selectorHash = {};
  
          /*   Function: verifyContains
              Verifies whether the element specified by the userEvent.selector contains the text stored in userEvent.text
  
            Parameters:
              userEvent - Object, a single DOM event from the JSON playback file.
  
            Returns:
              Boolean - true if the element does contain the specified text or false if it does not.
          */
          var verifyContains = function(userEvent) {
  
            var elementText = $(userEvent.selector).val() || $(userEvent.selector)[0].innerHTML;
  
            if (elementText.indexOf(userEvent.text) !== -1) {
              console.log("PASS - element does contain specified text.");
            } else {
              throw new Error("FAIL - element does not contain specified text.");
            }
          };
  
          /*  Function: simulateEvent
              Replays the DOM event specified by userEvent -- uses the same event type and same coordinates that were originally recorded for the event.
  
            Parameters:
              userEvent - Object, a single DOM event from the JSON playback file.
  
            Returns:
              Nothing.
          */
          var simulateEvent = function(self, userEvent) {
            if (userEvent.relatedSelector) {
              userEvent.relatedTarget = $(userEvent.relatedSelector)[0];
            }
  
            if (userEvent.selector in selectorHash) {
              var eventTarget = selectorHash[userEvent.selector];
            } else {
  
              if (userEvent.selector === "document") {
                var eventTarget = document;
              } else {
                var eventTarget = $(userEvent.selector)[0];
                if (userEvent.selector && !eventTarget) {
                  if (self.fail_time) {
                    if (window.performance.now() - self.fail_time > 5000) {
                      self.finished("FAIL getting - " + userEvent.selector);
                      return "error";
                    }
                  } else
                    self.fail_time = window.performance.now();
  
                  console.warn("Try Again", userEvent, window.performance.now() - self.fail_time);
                  return "again";
                }
              }
  
              if (userEvent.hasOwnProperty("clientX") && userEvent.hasOwnProperty("clientY")) {
  
                // get the target based on the click coordinates
                var target = document.elementFromPoint(userEvent.clientX, userEvent.clientY);
  
                // verify that the target from the coordinates matches the logged CSS selector
                if (target === eventTarget) {
                  console.log("PASS - click target matches selector element.");
                  selectorHash[userEvent.selector] = eventTarget;
                } else {
                  if ($(target).closest(eventTarget).length) {
                    console.log("PASS - click target matches selector parent element.");
                  } else {
                    if (self.fail_time) {
                      if (window.performance.now() - self.fail_time > 5000) {
                        self.finished("FAIL - Element at point (" + userEvent.clientX + "px, " + userEvent.clientY + "px) does not match selector " + userEvent.selector);
                        return "error";
                      }
                    } else
                      self.fail_time = window.performance.now();
  
                    console.warn("Try Again", userEvent, window.performance.now() - self.fail_time);
                    return "again";
                  }
                }
              }
            }
  
            self.fail_time = 0;
  
            console.log("Simulating event (" + (userEvent.timeStamp / 1000).toFixed(3) + "s). Selector: " + userEvent.selector + " Type: " + userEvent.type, userEvent);
  
            var event = null;
  
            switch (userEvent.type) {
              case "scroll":
                $(eventTarget).scrollLeft(userEvent.scrollLeft);
                $(eventTarget).scrollTop(userEvent.scrollTop);
                break;
              case "focusout":
              case "focusin":
              case "focus":
              case "blur":
                event = new FocusEvent(userEvent.type, userEvent);
                break;
              case "tap":
              case "click":
              case "dblclick":
              case "mouseup":
              case "mousedown":
              case "contextmenu":
                event = new MouseEvent(userEvent.type, userEvent);
                break;
              case "touchstart":
              case "touchend":
              case "touchmove":
              case "touchcancel":
  
                var touchList = [];
                for (var i = 0; i < userEvent.touches.length; i++) {
                  var touch = userEvent.touches[i];
                  var newTouch = new Touch({
                    "clientX": touch.clientX,
                    "clientY": touch.clientY,
                    "force": touch.force,
                    "identifier": touch.identifier,
                    "pageX": touch.pageX,
                    "pageY": touch.pageY,
                    "radiusX": touch.radiusX,
                    "radiusY": touch.radiusY,
                    "rotationAngle": touch.rotationAngle,
                    "screenX": touch.screenX,
                    "screenY": touch.screenY,
                    "target": $(touch.selector)[0]
                  });
                  touchList.push(newTouch);
                }
  
                userEvent.touches = touchList;
  
                var touchList = [];
                for (var i = 0; i < userEvent.changedTouches.length; i++) {
                  var touch = userEvent.changedTouches[i];
                  var newTouch = new Touch({
                    "clientX": touch.clientX,
                    "clientY": touch.clientY,
                    "force": touch.force,
                    "identifier": touch.identifier,
                    "pageX": touch.pageX,
                    "pageY": touch.pageY,
                    "radiusX": touch.radiusX,
                    "radiusY": touch.radiusY,
                    "rotationAngle": touch.rotationAngle,
                    "screenX": touch.screenX,
                    "screenY": touch.screenY,
                    "target": $(touch.selector)[0]
                  });
                  touchList.push(newTouch);
                }
  
                userEvent.changedTouches = touchList;
                event = new TouchEvent(userEvent.type, userEvent);
                break;
  
              case "keydown":
                event = new KeyboardEvent(userEvent.type, userEvent);
                if (eventTarget) {
                  if (document.activeElement != eventTarget)
                    eventTarget.focus();
  
                  if (userEvent.selectionRange) {
                    var v = userEvent.selectionRange.split("|");
                    eventTarget.setSelectionRange(parseInt(v[0]), parseInt(v[1]));
                  }
                }
                break;
              case "keyup":
              case "keypress":
                event = new KeyboardEvent(userEvent.type, userEvent);
                break;
              case "input":
                event = new Event(userEvent.type, userEvent);
                switch (eventTarget.tagName) {
                  case "INPUT":
                    eventTarget.value = userEvent.value;
                    break;
  
                  case "TEXTAREA":
                    console.log("record textarea");
                    break;
  
                  case "SELECT":
                    console.log("record select");
                    break;
  
                  default:
                    eventTarget.innerHTML = userEvent.value;
                }
                //$(userEvent.selector).val(userEvent.value, true);
                break;
              case "change":
                event = new Event(userEvent.type, userEvent);
                break;
              case "contains":
                verifyContains(userEvent);
                return;
              case "dragdrop":
                DndSimulator.simulate(userEvent.src, userEvent.dest, userEvent.copy);
                return;
              default:
                self.finished("Unsupported event type.");
                return "error"
            }
  
            if (event !== null && eventTarget) {
              eventTarget.dispatchEvent(event);
            }
  
          };
  
  
          /*  Playback constructor function. Unlike recording, to playback a test the user must
            create a new instance of the playback constructor and manually start it.
  
            Parameters:
              script - String, a json description of the playbacks script.
              finished - a callback when the interaction as finished
          */
          var constructor = function(script, finished) {
  
            var self = this;
  
            /*  this.window
                Object, stores the width and height attributes that the playback JSON file was designed to run in. It is essential
                that the playback occur in a web browser window with the same dimensions as the original test run recording.
            */
            this.window = null;
            this.finished = finished;
  
            /*  Property: this.userEventLog
                Array of events, this is where the recorded events are stored. Each event contains most standard event properties as well as
                some additional properties (selector and text) used for identifying the element and the contents of the element. The events are ordered
                oldest to newest (i.e., the events that were recorded first are at the beginning of the array).
            */
            this.userEventLog = null;
  
            playbackData = JSON.parse(script);
  
            // Validate the playback file we've received
            if (typeof playbackData == "object") {
  
              // We won't run the playback file without the window attributes (i.e., browser window dimensions)
              if (typeof playbackData.window == "object") {
                self.window = playbackData.window;
              } else {
                throw new Error("Playback JSON file does not contain required window attributes.");
              }
  
              // Verify that the event_log is an array, if it's not an array, then this is an invalid playback JSON file.
              if (Array.isArray(playbackData.event_log)) {
                self.userEventLog = playbackData.event_log;
              } else {
                throw new Error("Event log in the JSON playback file is not an array.");
              }
            } else {
              throw new Error("Received an invalid playback JSON file.");
            }
          };
  
          constructor.prototype = {
  
            /*  Method: start
                This method will start the playback of the user event log.
            */
            "start": function() {
  
              var self = this;
  
              if (playbackInProgress !== false) {
                self.finished("Cannot start playback -- there is another test playback already in-progress.");
                return;
              }
  
              if (recordInProgress !== false) {
                self.finished("Cannot start playback -- a recording is already in-progress.");
                return;
              }
  
              if (window.innerHeight !== this.window.height || window.innerWidth !== this.window.width) {
                self.finished("Cannot start playback -- browser window must match dimensions that the playback script was recorded in (" + this.window.width + "px by " + this.window.height + "px). Window is currently " + window.innerWidth + "px by " + window.innerHeight + "px.");
                return;
              }
  
              console.log("Starting test script playback.");
  
              playbackInProgress = true;
              selectorHash = {};
  
              function call_next() {
                while (self.userEventLog.length) {
                  var userEvent = self.userEventLog.shift();
                  var result = simulateEvent(self, userEvent);
                  if (result === "error") {
                    console.log("Test script playback error.");
                    playbackInProgress = false;
                    return;
                  }
  
                  if (result === "again") {
                    self.userEventLog.unshift(userEvent);
                    setTimeout(call_next, 100);
                    return;
                  }
                  if (self.userEventLog.length) {
                    if (self.userEventLog[0].timeStamp > 10 || self.userEventLog[0].type == "blur") {
                      setTimeout(call_next, Math.min(self.userEventLog[0].timeStamp, 400));
                      return;
                    }
                  } else {
                    console.log("Test script playback finished.");
                    playbackInProgress = false;
                    self.finished(true);
                  }
                }
              }
              call_next();
            }
          }
          return constructor;
        })()
  
        ,
      "record": (function() {
  
        var userEventLog = [];
        var ctrlKeyDown = false;
        var lastTimeStamp = 0;
        var dragElement;
  
        /*  Function: _getSelectionText
            This function will retrieve the value of the text currently selected by the user.
  
          Returns: String
        */
        var _getSelectionText = function() {
          var text = "";
          var activeEl = document.activeElement;
          var activeElTagName = activeEl ? activeEl.tagName.toLowerCase() : null;
          if (
            (activeElTagName == "textarea") || (activeElTagName == "input" &&
              /^(?:text|search|password|tel|url)$/i.test(activeEl.type)) &&
            (typeof activeEl.selectionStart == "number")
          ) {
            text = activeEl.value.slice(activeEl.selectionStart, activeEl.selectionEnd);
          } else if (window.getSelection) {
            text = window.getSelection().toString();
          }
          return text;
        };
  
        var _getSelection = function() {
          var result = null;
          var activeEl = document.activeElement;
          var activeElTagName = activeEl ? activeEl.tagName.toLowerCase() : null;
          if (
            (activeElTagName == "textarea") || (activeElTagName == "input" &&
              /^(?:text|search|password|tel|url)$/i.test(activeEl.type)) &&
            (typeof activeEl.selectionStart == "number")
          ) {
            result = "" + activeEl.selectionStart + "|" + activeEl.selectionEnd;
          }
          return result;
        }
  
        /*  Function: logEvent
            This function will parse the
  
        */
        var logEvent = function(event) {
  
          // Only record the event if recording is in progress
          if (recordInProgress == true) {
  
            try {
              wrong
            } catch (e) {
              stack_size = e.stack.split("\n").length;
              if (stack_size > 3) {
                // A generated event -> don't log
                console.log("Don't log generated event", stack_size, e)
                return;
              }
            }
  
            var userEvent = {
              "selector": getSelector(event.target)
            };
            if (event.relatedTarget)
              userEvent.relatedSelector = getSelector(event.relatedTarget);
  
            if (event.type === "scroll") {
              userEvent.type = "scroll";
              userEvent.scrollTop = $(event.target).scrollTop();
              userEvent.scrollLeft = $(event.target).scrollLeft();
              userEvent.timeStamp = event.timeStamp;
            } else {
              for (var prop in event) {
                // We can only record plain such as string, numbers and booleans in JSON. Objects will require special processing.
                if (["number", "string", "boolean"].indexOf(typeof event[prop]) > -1
                  // Exclude certain event event attributes in order to keep the JSON log as small as possible.
                  // These attributes are not needed to re-create the event during playback.
                  &&
                  ["AT_TARGET", "BUBBLING_PHASE", "CAPTURING_PHASE", "NONE", "DOM_KEY_LOCATION_STANDARD", "DOM_KEY_LOCATION_LEFT", "DOM_KEY_LOCATION_RIGHT", "DOM_KEY_LOCATION_NUMPAD"].indexOf(prop) == -1) {
                  userEvent[prop] = event[prop];
                } else if (["touches", "changedTouches"].indexOf(prop) > -1) {
  
                  userEvent[prop] = [];
  
                  for (var i = 0; i < event[prop].length; i++) {
                    var touch = event[prop][i];
                    userEvent[prop].push({
                      "clientX": touch.clientX,
                      "clientY": touch.clientY,
                      "force": touch.force,
                      "identifier": touch.identifier,
                      "pageX": touch.pageX,
                      "pageY": touch.pageY,
                      "radiusX": touch.radiusX,
                      "radiusY": touch.radiusY,
                      "rotationAngle": touch.rotationAngle,
                      "screenX": touch.screenX,
                      "screenY": touch.screenY,
                      "selector": getSelector(touch.target)
                    });
                  }
                }
              }
            }
  
            if (userEventLog.length) {
              var ts = userEvent.timeStamp;
              userEvent.timeStamp -= lastTimeStamp;
              lastTimeStamp = ts;
            } else {
              lastTimeStamp = userEvent.timeStamp;
              userEvent.timeStamp = 0;
            }
  
            if (userEvent.selector !== null) {
              if (playbackInProgress == false) {
                userEventLog.push(userEvent);
                console.log("Logged " + userEvent.type + " event. " + userEvent.timeStamp);
              }
            } else {
              console.warn("Null selector");
            }
          }
        };
  
        /*  Function: getSelector
            This function starts at the DOM element specified by 'el' and traverses upward through the DOM tree building out a unique
            CSS selector for the DOM element 'el'.
  
          Parameters:
            el - DOM element, the element that we want to determine CSS selector
            names - Array of strings, records the CSS selectors for the target element and parent elements as we progress up the DOM tree.
  
          Returns:
            String, a unique CSS selector for the target element (el).
        */
        var getSelector = function(el, names) {
          if (el === document || el === document.documentElement) return "document";
          if (el === document.body) return "body";
          if (typeof names === "undefined") var names = [];
          if (el.id) {
            names.unshift('#' + el.id);
            return names.join(" > ");
          } else if (el.className) {
            var arrNode = [].slice.call(el.parentNode.getElementsByClassName(el.className));
            var classSelector = el.className.split(" ").filter(Boolean);
  
            var c, i, index, len, ref;
            ref = ["droparea", "ui-state-focus", "is-cursor"];
            for (i = 0, len = ref.length; i < len; i++) {
              c = ref[i];
              index = classSelector.indexOf(c);
              if (index >= 0) {
                classSelector.splice(index, 1);
              }
            }
  
            classSelector = classSelector.join(".");
            if (arrNode.length == 1) {
              names.unshift(el.tagName.toLowerCase() + "." + classSelector);
            } else {
              for (var c = 1, e = el; e.previousElementSibling; e = e.previousElementSibling, c++);
              names.unshift(el.tagName.toLowerCase() + ":nth-child(" + c + ")");
            }
          } else {
            for (var c = 1, e = el; e.previousElementSibling; e = e.previousElementSibling, c++);
            names.unshift(el.tagName.toLowerCase() + ":nth-child(" + c + ")");
          }
  
          if (el.parentNode !== document.body) {
            getSelector(el.parentNode, names)
          }
          return names.join(" > ");
        };
  
        document.addEventListener('dblclick', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('click', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('contextmenu', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('mousedown', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('mouseup', function(event) {
          logEvent(event);
  
          // if the user has selected text, then we want to record an extra 'contains' event. on playback, this is used
          // to verify that the selected text is contained within the target element
          var selectedText = _getSelectionText();
          if (selectedText.length > 1) {
            logEvent({
              "target": document.activeElement,
              "type": "contains",
              "text": selectedText,
              "timeStamp": event.timeStamp
            });
          }
        }, true);
        document.addEventListener('change', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('input', function(event) {
          var extension = {};
          switch (event.target.tagName) {
            case "INPUT":
              extension.value = event.target.value;
              break;
  
            case "TEXTAREA":
              console.log("record textarea");
              break;
  
            case "SELECT":
              console.log("record select");
              break;
  
            default:
              extension.value = event.target.innerHTML;
          }
          logEvent($.extend(true, event, extension));
        }, true);
        document.addEventListener('focus', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('focusin', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('focusout', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('blur', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('keypress', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('keydown', function(event) {
          logEvent($.extend(true, event, {
            "selectionRange": _getSelection()
          }));
        }, true);
        document.addEventListener('keyup', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('touchstart', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('touchend', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('touchmove', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('touchcancel', function(event) {
          logEvent(event);
        }, true);
        document.addEventListener('scroll', function(event) {
          logEvent(event);
        }, true);
  
        document.addEventListener("drop", function(event) {
          console.log("drop!!")
          if (dragElement) {
            logEvent({
              "copy": event.ctrlKey,
              "src": dragElement,
              "dest": getSelector(event.srcElement),
              "target": event.target,
              "type": "dragdrop",
              "timeStamp": event.timeStamp
            });
            dragElement = null;
          }
        }, true);
  
        document.addEventListener("drag", function(event) {
          dragElement = getSelector(event.srcElement);
        }, true);
  
  
        return {
  
          /*  Method: start
              When this method is invoked, jsReplay will begin to record all user events that occur on the web page.
          */
          "start": function() {
            if (playbackInProgress == false) {
  
              console.log("Start recording.");
              dragElement = null;
              startTimeDelay = 0;
              userEventLog = [];
              recordInProgress = true;
  
            } else {
              throw new Error("Cannot start recording -- test playback is in progress.");
            }
          },
  
          /*  Method: stop
              When this method is invoked, jsReplay will stop recording user events and print playback JSON script to the console.
          */
          "stop": function() {
  
            console.log("Stop recording.");
  
            recordInProgress = false;
            userEventLog.splice(-2, 2); // remove the stop command.
  
            var playbackScript = {
              "window": {
                "width": window.innerWidth,
                "height": window.innerHeight
              },
              "event_log": userEventLog
            };
  
            return JSON.stringify(playbackScript);
          }
        };
      })()
    };
  })();
  