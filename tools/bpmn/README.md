# BPMN diagrams for class 2

## Class 3 drafts

```sh
python3 tools/bpmn/class3.py
node tools/bpmn/render.mjs 2026-2027/vjezbe/class3/bpmn-class3
```

The optional renderer argument selects a diagram folder containing
`manifest.json` and skips the class 2 derived views. Without an argument,
the existing class 2 workflow is unchanged. The class 3 generator checks
unique XML IDs and local references before writing each model.
Class 3 models are conceptual examples, not configured for deployment.

## Class 2 workflow

The editable sources are BPMN 2.0 XML files in
`2026-2027/vjezbe/class2/bpmn-class2/`. Open them in Camunda Modeler or
https://demo.bpmn.io/. They are conceptual models with
`isExecutable=false`, without Camunda execution settings.

bpmn-js renders the BPMN symbols from XML. The source files include
layout coordinates so the diagrams keep the same arrangement when
regenerated.

Run these commands from the repository root:

```sh
npm ci --prefix tools/bpmn
./tools/bpmn/node_modules/.bin/playwright install chromium
python3 tools/bpmn/generate.py
node tools/bpmn/render.mjs
make 2026-2027/vjezbe/class2/class2.html 2026-2027/vjezbe/class2/class2.pdf
```

To use an installed Chromium executable, set `BPMN_BROWSER` when running
the renderer:
`BPMN_BROWSER=/absolute/path/to/chromium node tools/bpmn/render.mjs`.
The renderer exports SVG and 2x PNG files and records BPMN import
warnings in `validation.json`.

Slides use the vector SVG files. Pandoc needs `rsvg-convert` from librsvg
to convert them for PDF output. The catalogue uses PNG previews.
Regenerating the diagrams requires npm and Chromium; building the slides
from the exported files does not require a browser.

`generate.py` defines the BPMN elements and their layout. Edit the lesson
Markdown and handout directly; `make preview` rebuilds the HTML on save.
`slides.py` is the original draft generator and requires `--overwrite`
to replace existing Markdown. To keep a direct Modeler edit, run only `render.mjs`:
regenerating the XML overwrites edits made in Modeler.

Run `node tools/bpmn/audit.mjs` to check image loading and slide overflow
in HTML. It writes screenshots and a contact sheet to `/tmp`.

The `wrong-*` models and `26-*` demonstrate mistakes for students to
find. Importing a model successfully checks the document and rendering;
it does not establish that the model meets its business requirements.
Starter models and collapsed subprocess views leave some details for
students to fill in.

Solution A is `17-base-overview.bpmn`; solution B is
`19-shared-deadline-solution.bpmn`. The deck shows each solution after
its task. The small examples are `20-*` through `25-*`. `28-*` is the
individual exit check, reused for recall the following week. Student
handouts contain requirements and starter diagrams without solutions.
The catalogue and deck include solutions for the discussion afterward.
The optional supplier example uses a receive task with a boundary timer.

The coloured views use `34-and-execution.bpmn`. They show both checks
running, one complete while the join waits for the other, and the shared
continuation after both finish. Blue highlights only ongoing work. Text labels identify completed work,
waiting and work that has not started; other flows stay neutral. The colours are teaching annotations, not extra BPMN notation or
an execution simulation. Whole sequence flows and arrowheads use the
same colour.

`views.json` records each view's source. View 31 is a crop of solution B.
View 32 uses a collapsed subprocess and a compact arrangement to show
the normal and manual continuations; the complete solution also shows
the error and reminder paths.

Archived versions v1-v4 have separate diagram folders and are not
regenerated. They are stored in
`2026-2027/vjezbe/class2/archive/`, with their diagrams and styles.

Renderer: https://bpmn.io/toolkit/bpmn-js/
License: https://bpmn.io/license

Reference sheets 36–39 introduce gateway, task and event types. Model 40
shows why a terminate end is wrong for a reminder. In solution B the
article code is validated before checking availability; an invalid code
interrupts any budget check still running in the same subprocess.

Notifications, reminders and requests to correct an application are service
tasks: the system calls a notification service. The intermediate-event
reference sheet includes message, timer and signal catch events.
