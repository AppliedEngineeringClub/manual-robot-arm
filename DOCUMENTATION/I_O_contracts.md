# Module I/O Contracts

The project is being reorganized into smaller modules under the `app` package. This document describes the responsibilities and input/output contracts of each module so contributors can work consistently.

## `app/config.py`
- **Purpose:** Centralize configuration values used across the UI.
- **Exports:** Immutable constants (window dimensions, FPS cap, dot colors, speeds, key mapping defaults).
- **Imports:** None (standard library only).
- **Consumers:** `app.app`, `app.state`, `app.controller`, `app.renderer`.
- **Notes:** No runtime logic; values should not be mutated elsewhere.

## `app/state.py`
- **Purpose:** Hold mutable state objects shared across the application.
- **Exports:**
  - `DotState`: current dot position (`x`, `y`), radius, and color.
  - `AppState`: top-level container (`running`, `surface`, `clock`, `dot`, plus future elements like claw state).
  - `initial_state()` helper to construct a fresh `AppState`.
- **Imports:** `app.config` for default values.
- **Consumers:** `app.app` creates/owns the state; `app.controller` mutates it; `app.renderer` reads it.
- **Notes:** Should not import Pygame directly other than typing hints.

## `app/input.py`
- **Purpose:** Translate raw input (keyboard, gamepad later) into a structured representation for the controller.
- **Exports:** `poll_keyboard()` returning a `ControllerInput` dataclass or dict with flags (`left`, `right`, `forward`, `backward`, `up`, `down`, etc.).
- **Imports:** `pygame`.
- **Consumers:** `app.app` (or indirectly `app.controller`) each frame.
- **Notes:** Must not mutate `AppState`; pure input reading.

## `app/controller.py`
- **Purpose:** Apply game logic, updating state from user input.
- **Exports:** `update(state: AppState, controls: ControllerInput, dt: float = 0.0) -> None`.
- **Imports:** `app.config` for bounds/speeds.
- **Consumers:** `app.app` calls `update` once per frame.
- **Notes:** No direct drawing or Pygame calls; all changes happen via `state` mutation.

## `app/renderer.py`
- **Purpose:** Draw the current state to the screen.
- **Exports:** `render(state: AppState) -> None` (or `render(surface, state)` if preferred).
- **Imports:** `pygame`, `app.config` (for colors if needed).
- **Consumers:** `app.app` calls once per frame after updates.
- **Notes:** Reads state and draws to `state.surface`; no state mutation besides drawing.

## `app/app.py`
- **Purpose:** High-level orchestration of initialization, event handling, update loop, and cleanup.
- **Exports:** `App` class with methods:
  - `on_init() -> bool`
  - `on_event(event)`
  - `on_loop(dt)`
  - `on_render()`
  - `on_execute()` / `run()`
- **Imports:** `pygame`, `app.config`, `app.state`, `app.input`, `app.controller`, `app.renderer`.
- **Consumers:** Entry point (`pygame_window.py`) instantiates and runs `App`.
- **Notes:** Owns the `AppState` instance and the main loop; no business logic beyond coordinating modules.

## `pygame_window.py`
- **Purpose:** Lightweight entry point for running the UI.
- **Behavior:** Imports `App`, constructs it, and calls `on_execute()` (or `run()`), returning an exit code.
- **Notes:** Should remain minimal to keep the project testable.

## Future Modules (examples)
- `app/claw.py`: If the claw state grows complex, move its logic here.
- `transport/bluetooth.py`: Encapsulate Bluetooth transport without coupling it to the UI modules.

Keeping these contracts explicit helps new contributors understand how data flows through the UI and prevents accidental tight coupling between modules.

