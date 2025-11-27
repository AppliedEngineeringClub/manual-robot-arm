# File Ownership Assignments

These assignments reflect the current responsibilities after the codebase restructuring. Files were reorganized from the original modular structure into a simpler design.

| File | Owner | Previous File (if applicable) |
| --- | --- | --- |
| `app/main.py` | **Vince** | `app/app.py` |
| `app/ball_input.py` | **Richard** | `app/input.py` |
| `app/ball_struct.py` | **Anderson** | `app/state.py` (+ controller logic) |
| `app/render.py` | **Nicole** | `app/renderer.py` |

**Note:** The following files from the previous structure no longer exist:
- `app/config.py` (was J/Julian's) - configuration values are now inline
- `app/controller.py` (was Justin's) - controller logic is now in `ball_struct.py`


> Update this document if responsibilities change so the team knows who to contact for reviews or questions.

