# SVG Process Flow Diagram — Creation Guide for AI Agents

> A step-by-step playbook for generating clean, editable, Confluence-ready SVG process flow diagrams.
> Based on the proven approach used for the Pilot-to-ACM Handover Wizard diagram.

---

## 1. When to Use This Guide

Use this approach when a user asks for:
- Process flow diagrams
- Swim lane diagrams
- System architecture flows
- Step-by-step workflow visualizations

**Output format:** Raw SVG file (`.svg`). No external tools or libraries needed — just XML.

---

## 2. Planning Phase

Before writing any SVG, answer these questions:

### 2a. Identify the Actors (Swim Lanes)
List all actors/systems involved. Each becomes a vertical swim lane.

| Example | Lanes |
|---------|-------|
| Handover Wizard | Flow (Automation), AE (Wizard), ACM (Task) |
| CI/CD Pipeline | Developer, GitHub Actions, Staging, Production |
| Approval Process | Requester, Manager, System |

**Rule:** Keep to 2-4 swim lanes. More than 4 makes the diagram too wide.

### 2b. Map the Steps
Write out each step as a simple list:
```
1. [Actor] does X
2. [System] creates Y
3. [Actor] sees Z
...
```

### 2c. Identify Annotations
Separate the "what happens" (main flow) from "how it works" (implementation details):
- **Main flow:** boxes + arrows
- **Annotations:** dashed callout bubbles (SLA points, save behavior, resume capability, etc.)

---

## 3. SVG Structure Template

### 3a. Root Element
```xml
<svg xmlns="http://www.w3.org/2000/svg"
     width="2400" height="1840"
     viewBox="0 0 1200 920"
     font-family="Segoe UI, Helvetica, Arial, sans-serif"
     font-size="13">
```

**Key sizing rules:**
- `viewBox` defines the internal coordinate system (design at 1200x920 or similar)
- `width`/`height` set the rendered size — use **2x the viewBox** for Confluence readability
- If the diagram has more steps, increase viewBox height proportionally (add ~80-100px per step)

### 3b. Defs Block (Reusable Components)
Always include at the top:
```xml
<defs>
  <!-- Standard arrow marker -->
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
  </marker>
  <!-- Colored arrow for primary flow -->
  <marker id="arrow-blue" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#0070d2"/>
  </marker>
  <!-- Drop shadow filter -->
  <filter id="shadow" x="-2%" y="-2%" width="104%" height="104%">
    <feDropShadow dx="1" dy="1" stdDeviation="2" flood-opacity="0.1"/>
  </filter>
</defs>
```

### 3c. Section Comments
**Always** use clear section comments. This is what makes the SVG editable:
```xml
<!-- ==================== SWIM LANE HEADERS ==================== -->
<!-- ==================== FLOW LANE ==================== -->
<!-- ==================== AE LANE ==================== -->
<!-- ==================== ACM LANE ==================== -->
<!-- ==================== LEGEND ==================== -->
```

Every element should also have a short comment above it:
```xml
<!-- AE Opens Task -->
<rect .../>
```

---

## 4. Visual Component Library

### 4a. Swim Lane Background
Full-height colored rectangle with low opacity:
```xml
<rect x="20" y="58" width="130" height="830" rx="6" fill="#e8eaf6" opacity="0.5"/>
<text x="85" y="80" text-anchor="middle" font-size="12" font-weight="700" fill="#3949ab">LANE NAME</text>
<text x="85" y="94" text-anchor="middle" font-size="10" fill="#3949ab">(Subtitle)</text>
```

### 4b. Trigger / Event (Rounded Pill)
For events that initiate a process:
```xml
<rect x="30" y="115" width="110" height="52" rx="20" fill="#7986cb" filter="url(#shadow)"/>
<text x="85" y="137" text-anchor="middle" font-size="11" fill="white" font-weight="600">Event Name</text>
<text x="85" y="153" text-anchor="middle" font-size="10" fill="white">Detail</text>
```
- `rx="20"` gives the pill/rounded shape
- Use for: triggers, stage changes, external events

### 4c. System Action (Rectangle)
For automated steps:
```xml
<rect x="30" y="200" width="110" height="62" rx="4" fill="#5c6bc0" filter="url(#shadow)"/>
<text x="85" y="220" text-anchor="middle" font-size="10" fill="white" font-weight="600">System Does:</text>
<text x="85" y="235" text-anchor="middle" font-size="10" fill="#e8eaf6">Detail line 1</text>
<text x="85" y="249" text-anchor="middle" font-size="10" fill="#e8eaf6">Detail line 2</text>
```
- `rx="4"` gives a subtle rounded corner (not a pill)
- Use for: flow actions, system creates/updates

### 4d. User Action (Solid Colored Rectangle)
For user-performed steps:
```xml
<rect x="200" y="208" width="180" height="46" rx="6" fill="#1976d2" filter="url(#shadow)"/>
<text x="290" y="228" text-anchor="middle" font-size="12" fill="white" font-weight="600">Action Name</text>
<text x="290" y="243" text-anchor="middle" font-size="10" fill="#bbdefb">Subtitle</text>
```

### 4e. Wizard Step / Process Step (Card with Header)
For multi-step processes — gives a "card" look with a colored header:
```xml
<rect x="175" y="358" width="230" height="54" rx="6" fill="white" stroke="#42a5f5" stroke-width="2" filter="url(#shadow)"/>
<rect x="175" y="358" width="230" height="20" rx="6" fill="#42a5f5"/>
<rect x="175" y="368" width="230" height="10" fill="#42a5f5"/>
<text x="290" y="373" text-anchor="middle" font-size="11" fill="white" font-weight="700">STEP 1: Name</text>
<text x="290" y="398" text-anchor="middle" font-size="10" fill="#555">Description of this step</text>
```
- Three overlapping rects create the header band effect
- Use for: wizard steps, pipeline stages, process phases

### 4f. Annotation Callout (Dashed Rounded Pill)
For implementation details, SLA points, technical notes:
```xml
<rect x="430" y="330" width="210" height="44" rx="16" fill="#fff3e0" stroke="#ff9800" stroke-width="1" stroke-dasharray="4,3"/>
<text x="535" y="348" text-anchor="middle" font-size="10" fill="#e65100" font-weight="600">Feature Name</text>
<text x="535" y="362" text-anchor="middle" font-size="9" fill="#bf360c">Detail description</text>
```
- `stroke-dasharray="4,3"` makes it dashed
- `rx="16"` gives a soft rounded shape
- Connect with a dashed line to the relevant step

### 4g. Apex/Code Method Call (Outlined Rectangle)
For showing specific method invocations:
```xml
<rect x="200" y="282" width="180" height="46" rx="6" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5" filter="url(#shadow)"/>
<text x="290" y="302" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="600">methodName()</text>
<text x="290" y="317" text-anchor="middle" font-size="10" fill="#555">What it does</text>
```

---

## 5. Connecting Elements

### 5a. Solid Arrow (Main Flow)
```xml
<line x1="290" y1="254" x2="290" y2="282" stroke="#0070d2" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
```

### 5b. Solid Arrow with Label
```xml
<line x1="290" y1="412" x2="290" y2="440" stroke="#0070d2" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
<text x="305" y="430" font-size="9" fill="#0070d2" font-style="italic">Label</text>
```

### 5c. Dashed Line (Annotation Connector)
```xml
<line x1="405" y1="370" x2="430" y2="352" stroke="#ff9800" stroke-width="1" stroke-dasharray="4,3"/>
```

### 5d. Cross-Lane Arrow (Horizontal)
```xml
<line x1="140" y1="231" x2="200" y2="231" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
```

### 5e. L-Shaped Arrow (for non-direct connections)
Use three line segments:
```xml
<line x1="290" y1="662" x2="290" y2="690" stroke="#555" stroke-width="1" stroke-dasharray="3,3"/>
<line x1="290" y1="690" x2="130" y2="690" stroke="#555" stroke-width="1" stroke-dasharray="3,3"/>
<line x1="130" y1="690" x2="130" y2="646" stroke="#555" stroke-width="1" stroke-dasharray="3,3" marker-end="url(#arrow)"/>
```

---

## 6. Color Palette

Use consistent colors per actor/purpose:

| Purpose | Fill | Stroke | Text |
|---------|------|--------|------|
| **Automation/Flow** | `#7986cb` (pill), `#5c6bc0` (action) | — | white |
| **Primary Actor (e.g., AE)** | `#1976d2` (action), `#e3f2fd` (method) | `#1976d2` | white / `#1565c0` |
| **Wizard Steps** | white | `#42a5f5` | `#555` body |
| **Secondary Actor (e.g., ACM)** | `#2e7d32` (action), `#388e3c` (dark) | `#66bb6a` | white / `#c8e6c9` |
| **SLA Callout** | `#fce4ec` | `#e91e63` | `#880e4f` |
| **Feature Callout** | `#fff3e0` | `#ff9800` | `#e65100` |
| **Resume/State Callout** | `#f3e5f5` | `#9c27b0` | `#6a1b9a` |
| **Time/Metric Callout** | `#e0f7fa` | `#00838f` | `#00695c` |
| **Background** | `#f7f8fa` | — | — |
| **Lane Background** | Use actor color at `opacity="0.4-0.5"` | — | — |

---

## 7. Legend Block

Always include a legend in the top-right area:
```xml
<rect x="700" y="115" width="470" height="170" rx="8" fill="white" stroke="#ddd" stroke-width="1" filter="url(#shadow)"/>
<text x="720" y="138" font-size="12" font-weight="700" fill="#333">Legend</text>

<!-- One entry per visual type used in the diagram -->
<rect x="720" y="150" width="60" height="22" rx="11" fill="#7986cb"/>
<text x="750" y="165" text-anchor="middle" font-size="9" fill="white">trigger</text>
<text x="795" y="165" font-size="10" fill="#555">Description of this element type</text>
```

**Rule:** Only include legend items for element types actually used in the diagram.

---

## 8. Layout Guidelines

### Spacing
- **Vertical gap between steps:** 28-30px
- **Step box height:** 46-58px depending on content lines
- **Lane width:** proportional to content (busiest lane gets most width)
- **Callout offset:** 20-30px from the connected element

### Positioning Strategy
1. Place swim lane backgrounds first (full height)
2. Place main flow elements top-to-bottom within each lane
3. Add cross-lane arrows
4. Add annotation callouts to the side of the main flow
5. Place legend in unused space (typically top-right)

### Text Rules
- **Title:** font-size="20", font-weight="700"
- **Lane headers:** font-size="12", font-weight="700"
- **Box titles:** font-size="11-12", font-weight="600"
- **Box details:** font-size="9-10"
- **Arrow labels:** font-size="9", font-style="italic"
- Always use `text-anchor="middle"` and center x on the parent rect's center

---

## 9. Confluence Embedding Checklist

- [ ] Set explicit `width` and `height` on the `<svg>` element (2x the viewBox dimensions)
- [ ] Verify the SVG opens correctly in a browser before uploading
- [ ] Upload as an attachment to the Confluence page
- [ ] Use the "Image" macro or drag-and-drop to embed
- [ ] If still too small in Confluence, increase the width/height multiplier to 2.5x or 3x

---

## 10. Editing the SVG After Creation

The section comments make targeted edits easy:

**To add a new step:**
1. Find the section comment for the relevant lane
2. Copy an existing step block
3. Adjust y-coordinates (shift down by step height + gap)
4. Update text content
5. Add connecting arrows

**To remove an element:**
1. Find its comment
2. Delete the comment + all elements until the next comment
3. Adjust y-coordinates of elements below (shift up)
4. Update connecting arrows

**To change wording:**
1. Find the `<text>` element by searching for the current text
2. Replace the text content between `>` and `</text>`

**To change an arrow's path:**
1. Find the `<line>` element
2. Adjust `x1,y1` (start) and `x2,y2` (end) coordinates

---

## 11. Reference Example

See the working example at:
`~/Desktop/handover-wizard-process-flow.svg`

This diagram demonstrates all component types:
- 3 swim lanes (Flow, AE, ACM)
- Trigger pills, system actions, user actions, wizard step cards
- Method call boxes, annotation callouts (4 types)
- Cross-lane arrows, labeled arrows, dashed connectors
- Legend with key objects list
