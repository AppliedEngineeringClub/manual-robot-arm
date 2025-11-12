# Manual Robot Arm – Control & Integration Plan

## 1. Objectives
- Transform the current Pygame demo into a control station for the manual robot arm.
- Stream directional/size inputs to an ESP32 over Bluetooth to drive actuators.
- Preserve a smooth user experience while maintaining safe motion limits.

## 2. Current State
- `pygame-window.py` renders a red dot and maps keyboard controls to continuous movement and size changes.
- No networking layer, data protocol, or firmware exists yet to control the physical arm.
- Repository is now tracked on GitHub at `AppliedEngineeringClub/manual-robot-arm`.

## 3. Target Architecture
| Component | Responsibility | Notes |
| --- | --- | --- |
| Pygame Control UI (Raspberry Pi) | Capture user input, visualize state, serialize commands | Runs `pygame-window.py`; will gain Bluetooth module |
| Command Protocol Layer | Translate dot position/scale into arm joint/actuator commands | Decide on absolute vs. relative moves; include rate limiting |
| Bluetooth Link | Reliable transport between Raspberry Pi and ESP32 | Evaluate classic SPP vs. BLE GATT |
| ESP32 Firmware | Parse commands, validate, drive actuators safely | Needs watchdog, safety limits, calibration routines |
| Actuator Drivers | Apply PWM / motor control signals | Depends on actuator type (servos, steppers, etc.) |

## 4. Work Plan
### Phase A – Foundation
- [ ] Document actuator specs (voltage, torque, control signal type).
- [ ] Prototype Bluetooth connectivity (`bleak` or `pybluez`) between Pi and ESP32 dev board.
- [ ] Define command schema (e.g., JSON `{ joint_id, velocity }` or compact binary).

### Phase B – Control Loop Enhancements
- [ ] Add state model to Pygame app (e.g., joint angles, gripper state).
- [ ] Map keyboard/gamepad input to meaningful commands (position, velocity, presets).
- [ ] Log outgoing command packets for debugging (`commands.log`).
- [ ] Implement emergency-stop and safe defaults.

### Phase C – ESP32 Firmware
- [ ] Set up FreeRTOS / Arduino framework.
- [ ] Implement Bluetooth receive handler and parser.
- [ ] Add actuator drivers (PWM/stepper control) with calibration offsets.
- [ ] Enforce safety limits and watchdog timeout (e.g., 200 ms).
- [ ] Provide feedback packets (ACK, fault code, telemetry).

### Phase D – Integration & Testing
- [ ] Build simulator harness: ESP32 loops messages back for validation.
- [ ] Integrate real actuators on test bench; measure response & latency.
- [ ] Tune control gains, velocity limits, smoothing filters.
- [ ] Conduct full robot arm dry run, then load tests.

### Phase E – Documentation & Release
- [ ] Expand README with setup for Bluetooth & hardware wiring.
- [ ] Draft troubleshooting guide (pairing issues, calibration errors).
- [ ] Tag release once end-to-end demo is stable.

## 5. Testing Strategy
- Unit tests for command serialization/deserialization.
- Integration test: replay recorded input sequences, verify ESP32 outputs.
- Hardware-in-loop (HIL) test: measure actual actuator motion vs. expected.
- Regression suite before each release.

## 6. Risks & Mitigations
| Risk | Mitigation |
| --- | --- |
| Unstable Bluetooth connection | Add retry logic, keep-alive packets, monitor RSSI |
| Unsynchronized control rates | Use fixed tick rates (e.g., 60 Hz UI, 50 Hz command) and timestamps |
| Safety violations (over-rotation) | Apply clamping in both UI and firmware; include emergency stop |
| Latency spikes causing jitter | Buffer commands, implement smoothing on ESP32 |

## 7. Next Actions
1. Choose the Bluetooth library and draft a minimal messaging prototype.
2. Define the command data model and document it in `/docs/`.
3. Set up an ESP32 sandbox project that can receive and echo commands.

## Appendix A – Splitting `pygame-window.py`
The current UI works as a single file, but refactoring it into focused modules will improve readability and testing. Follow the steps below and keep the code style (comments, naming) consistent with the existing implementation.

### Step-by-step order
1. **Create the package shell** – add `app/__init__.py`.
2. **Extract constants** – move window/dot constants into `app/config.py`.
3. **Add shared state objects** – create `app/state.py`.
4. **Extract keyboard polling** – add `app/input.py`.
5. **Extract movement logic** – add `app/controller.py`.
6. **Extract rendering** – add `app/renderer.py`.
7. **Move the `App` class** – place the loop inside `app/app.py`.
8. **Trim the entry point** – keep `pygame-window.py` as the launcher only.
9. Run `python3 pygame-window.py` after each step to verify nothing regresses.

### `app/config.py`
```python
##holds global configuration values for pygame window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 400
FPS_CAP = 60

##dot styling and movement defaults
DOT_COLOR = (255, 0, 0)
DOT_RADIUS_START = 10
DOT_RADIUS_MIN = 2
DOT_RADIUS_MAX = 40
DOT_SPEED = 5
DOT_RADIUS_STEP = 1
```

### `app/state.py`
```python
##lightweight containers for application state
from app import config

class DotState:
    def __init__(self):
        self.x = config.WINDOW_WIDTH // 2
        self.y = config.WINDOW_HEIGHT // 2
        self.color = config.DOT_COLOR
        self.radius = config.DOT_RADIUS_START

class AppState:
    def __init__(self):
        self.running = True
        self.clock = None
        self.surface = None
        self.dot = DotState()
```

### `app/input.py`
```python
##wraps pygame keyboard polling so it can be reused or swapped later
import pygame

def poll_keyboard():
    keys = pygame.key.get_pressed()
    return {
        "left": keys[pygame.K_LEFT],
        "right": keys[pygame.K_RIGHT],
        "up": keys[pygame.K_UP],
        "down": keys[pygame.K_DOWN],
        "grow": keys[pygame.K_z],
        "shrink": keys[pygame.K_x],
    }
```

### `app/controller.py`
```python
##updates dot position and size based on input flags
from app import config

def update(state, controls):
    dot = state.dot

    ##move dot left right, forward and backward by checking key press
    if controls["left"]:
        dot.x -= config.DOT_SPEED
    if controls["right"]:
        dot.x += config.DOT_SPEED
    if controls["up"]:
        dot.y -= config.DOT_SPEED
    if controls["down"]:
        dot.y += config.DOT_SPEED

    ##checks to see if z or x are pressed to go "up or down"
    if controls["grow"]:
        dot.radius = min(config.DOT_RADIUS_MAX, dot.radius + config.DOT_RADIUS_STEP)
    if controls["shrink"]:
        dot.radius = max(config.DOT_RADIUS_MIN, dot.radius - config.DOT_RADIUS_STEP)

    ##keep dot within window bounds
    dot.x = min(config.WINDOW_WIDTH - dot.radius, max(dot.radius, dot.x))
    dot.y = min(config.WINDOW_HEIGHT - dot.radius, max(dot.radius, dot.y))
```

### `app/renderer.py`
```python
##draws the current frame
import pygame

def render(state):
    surface = state.surface
    dot = state.dot

    ##Clears previous frame every time dot moves
    surface.fill((0, 0, 0))

    ##Draws red dot at new position
    pygame.draw.circle(surface, dot.color, (dot.x, dot.y), dot.radius)

    ##Updates display to show new dot position
    pygame.display.flip()
```

### `app/app.py`
```python
##high level application loop built from smaller modules
import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF

from app import config, state, input, controller, renderer

class App:
    def __init__(self):
        self.state = state.AppState()

    def on_init(self):
        pygame.init()
        self.state.surface = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            HWSURFACE | DOUBLEBUF
        )
        self.state.clock = pygame.time.Clock()
        self.state.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.state.running = False

    def on_loop(self):
        dt = self.state.clock.tick(config.FPS_CAP) / 1000
        controls = input.poll_keyboard()
        controller.update(self.state, controls)

    def on_render(self):
        renderer.render(self.state)

    def on_execute(self):
        if self.on_init() is False:
            self.state.running = False

        while self.state.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        pygame.quit()
```

### Updated `pygame-window.py`
```python
#!/usr/bin/env python3

import sys
from app.app import App

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
    sys.exit(0)
```

> **Reminder:** only the plan was updated here. When you implement the split, apply the snippets above to their respective files in the stated order.

