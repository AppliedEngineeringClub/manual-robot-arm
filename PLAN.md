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

