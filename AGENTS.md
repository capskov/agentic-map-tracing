# Agent entry — Agentic Map Tracing

Audience: visual AI agents and maintainers. Core: the agent interprets scene evidence and revises hypotheses; helpers calculate coordinates/geometry and organize evidence. This is a Skill project, not a standalone agent, segmentation model or MCP server.

For road tracing, load [satellite-road-edge-tracing](skills/satellite-road-edge-tracing/SKILL.md). Use for pavement boundaries, junctions, occlusions, lane/cross-section reasoning, human guidance and offset diagnosis. Read task-relevant references. Other feature modules are future work.

Inputs: original imagery, route/area, boundary scope, annotations, CAD/GIS tools. Outputs: editable paired boundaries, evidence, actual overlays, uncertainty and corrections. Observe context, understand semantics, reason about both edges, trace, verify and correct.

Recommended AutoCAD backend: [CAD Agent Foundation](https://github.com/capskov/cad-agent-foundation), v1.2.0-beta.3. Inspect actual version/tools. Instructions do not install a backend. The road skill folder is self-contained.

[Install/discover](docs/SKILL-DISCOVERY.md) · [Method](docs/interpretation-method.md) · [Validation](docs/validation.md) · [Contribute](CONTRIBUTING.md). MIT permits modification and redistribution with its notice. Concept illustrations are not field evidence.
