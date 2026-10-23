# Agentic Map Tracing

**Teach agents to reason about where a boundary belongs — and why.**

Agent-native skills for reasoning-driven satellite/aerial imagery interpretation and editable CAD/GIS tracing. **v0.1.0-beta.1** · [Agent entry](AGENTS.md) · [Install / 检索安装](docs/SKILL-DISCOVERY.md) · [Contribute / 共同改进](CONTRIBUTING.md)

Package experienced mappers’ observation, scene interpretation, domain knowledge, and iterative correction into executable agent skills.

**Observe → Understand → Reason → Trace → Verify → Correct**

[中文](README.md) · [Method](docs/interpretation-method.md) · [Correction cases](docs/correction-cases.md) · [Road skill](skills/satellite-road-edge-tracing/SKILL.md) · [Validation](docs/validation.md)

## Interpret the scene, then trace the boundary

Agentic Map Tracing is a skill project for agent-led interpretation and digitization of geospatial imagery. The visual agent observes, interprets, and decides. Available CAD/GIS tools turn decisions into editable geometry; small helpers handle coordinates, geometry, and evidence organization.

When trees hide a road edge, an experienced mapper examines clear sections farther along the road, markings, pavement transitions, entrances, and junction layout. Conflicting evidence prompts reconsideration. This project attempts to organize that process for an agent, with reviewable decisions and corrections.

The main deliverable is a method for **understanding features, selecting evidence, proposing geometric constraints, and revising mistaken interpretations**. Learning here means improving skills and helpers through human feedback, not automatically updating model weights.

**Road edges are the first field-used module.** Buildings, land cover, water features, and other objects are future directions, not implemented capabilities.

## What does the agent reason about?

| Scene | Interpretation task | Evidence limitation |
| --- | --- | --- |
| Tree-covered edges | Find clear sections before and after an occlusion; explain continuity and width together | A shadow boundary is not a pavement edge |
| Road markings | Distinguish lane dividers, edge lines, centerlines, and medians; inspect spacing and cross-section composition | Paint width is not lane width; markings may sit inside pavement |
| Junction widening | Interpret markings, arrows, islands, tapers, and stable widened sections | Widening cannot justify arbitrary curved outlines |
| Similar surface colors | Combine material transitions, curbs, cycle lanes, tree pits, and continuity | Similar color does not establish material |
| Cars or bicycles | Use position, direction, and activity space as contextual evidence | Parking may be informal or illegal |
| Buildings, walls, entrances | Check access and paved continuity between adjacent features | Walls need not parallel roads; roof edges are not road edges |
| Human reference lines | Interpret intended boundaries, direction, width, or uncertainty | Schematic endpoints are not survey points |
| Smooth but displaced lines | Review paired edges; separate registration, conversion, and semantic mistakes | Successful drawing does not establish alignment |

This is a workflow inspired by human mapping practice, not a newly validated model architecture. See the [method notes](docs/interpretation-method.md).

## Three principles

**Understand the whole feature before resolving a local edge.** Unclear pixels should trigger a wider context check. Enlargement adds no source detail; filters only aid observation.

**Use domain knowledge to constrain and challenge hypotheses.** Markings support direction and road composition. Regular sections share consistent geometry; supported tapers are separate. Typical dimensions check plausibility without forcing existing roads into nominal widths.

**Allow the agent to reject its own interpretation.** Preserve the old candidate, inspect contradictory evidence, and revise it. Review should include evidence not used to build the candidate.

![Self-made concept illustration; not a field extraction result](docs/road-band.svg)

## Correction is part of the result

A local trial interpreted a narrow visible gray strip under tree cover as a roughly **5.5 m** branch-road candidate. Checking the actual CAD window and human reference lines revealed a conflicting roughly **10 m** cross-section guide. The narrow candidate was withdrawn. Both widths were local imagery/guidance estimates, not survey measurements or defaults.

Another approach developed an unsupported vase-like outline as its edges independently followed brightness. The revision reinterpreted long-range markings and used a shared road band to separate a taper from the stable section.

These are **hypothesis → contradiction → further evidence → revised interpretation** narratives, documenting errors as well as corrections. See the [de-identified case notes](docs/correction-cases.md). Private imagery and actual CAD screenshots are excluded; conceptual drawings are not field evidence.

## Relationship to extraction tools

| Project | Primary focus |
| --- | --- |
| [SamGeo](https://github.com/opengeos/segment-geospatial) | SAM-based geospatial segmentation, interactive prompts, and vector outputs |
| [SAM-Road](https://github.com/htcr/sam_road) | Large-scale vector road-network extraction from aerial imagery |
| [SAM-Maps](https://github.com/tudelft-iv/sam-maps) | Road graphs, drivable-area segmentation, and connectivity combined into road maps |
| **Agentic Map Tracing** | **Skills for an agent’s scene interpretation, domain reasoning, editable tracing, and evidence-based correction** |

These are scope distinctions, not accuracy rankings. Existing methods also use context, domain priors, human intervention, and agent interfaces. This project explores organizing interpretation as a general visual agent’s workflow rather than shipping a dedicated segmentation network as its main deliverable.

Segmentation, filters, edge hints, and vectorization can assist. The agent explains why a boundary is accepted, where evidence conflicts, and what remains uncertain. No segmentation weights are bundled or required.

## Modules

| Module | Status |
| --- | --- |
| **Road Edge Tracing** | Available skill, real CAD iteration, and local user approval; no independent general benchmark |
| Sidewalks and curbs | Supporting interpretation within the road skill; standalone module planned |
| Buildings, walls, site boundaries | Future direction; no implemented module |
| Green areas, parking areas, water features | Future direction; no implemented module |

The repository is `agentic-map-tracing`. The existing road skill retains its invocation: `$satellite-road-edge-tracing`. Domain rules stay in the module; shared resources can be extracted when another implemented module needs them. No empty future-module directories are shipped.

## Environment and model recommendations

**Field work used zoom-level 18 satellite imagery, Codex as the agent host, and AutoCAD with an existing CAD tool adapter.** According to the author's field-use feedback, **GPT-6.1 Sol at Low reasoning effort can complete routine tracing tasks. Use it as the recommended starting point; lower-capability or lower-effort configurations are not recommended.** For difficult locations, increase effort to **XHigh**, or use an agent with stronger visual reasoning.

| Condition | Practical recommendation |
| --- | --- |
| Imagery | Zoom-level 18 was used; prefer genuinely higher effective resolution with clearer markings and surface boundaries |
| Routine sections | GPT-6.1 Sol at Low in Codex, with this skill and actual-overlay review |
| Difficult locations | Occlusion, channelization, multiple lanes, curves, ambiguous cross-sections, or repeated displacement: use XHigh and focus on that location |
| Stronger agents | Stronger visual understanding, spatial reasoning, and domain knowledge, combined with clear prompts and evidence, generally help on complex cases |

**Results depend heavily on the agent's reasoning and road knowledge.** Prompts should define the target boundary, long-range marking/cross-section evidence, paired placement, human guidance, and actual-overlay review. The skill organizes this work; it does not supply the agent's underlying perceptual capability.

Tile zoom level is not a uniform survey-accuracy measure. Higher levels help when they provide genuinely clearer source imagery; enlargement or interpolation alone adds no information. Stronger agents and XHigh still require output review.

These are field-use recommendations, not a controlled demonstration of a universal capability threshold or accuracy guarantee. Model choice and reasoning effort are separate; Low/XHigh describe effort settings. See the [official model documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

## Recommended execution backend / 推荐执行底座

For Windows/AutoCAD 2026, use [CAD Agent Foundation](https://github.com/capskov/cad-agent-foundation), with the scoped [v1.2.0-beta.3 preview](https://github.com/capskov/cad-agent-foundation/releases/tag/v1.2.0-beta.3). It supplies native reads, proxy geometry, digests, bounded drawing, views/captures, raster-path repair and save feedback. This Skill supplies scene interpretation, road decisions and visual correction.

在Windows/AutoCAD 2026环境推荐智能底座新版；其他等价CAD/GIS后端可适配。底座与Skill分别安装，均可按任务独立选择。Skill不是MCP服务器，不增加后端缺失的操作。路径修复不等于影像配准，代理几何不等于专业属性；截图色彩与显示稳定性限制须结合原图和实际窗口复核。

## Use the road module

The host needs skill loading, source-image inspection, and CAD/GIS read/write and screenshot tools. Field experience is from Codex with AutoCAD. Other hosts/adapters require validation. No connector or universal exporter is bundled. Skill/reference instructions are currently Chinese for a multilingual agent.

Copy `skills/satellite-road-edge-tracing` into your host’s skill directory. A common Codex location is `~/.codex/skills/`; use other hosts’ own loading conventions.

> Use $satellite-road-edge-tracing to trace carriageway edges at every crossing along this route. Inventory crossings, interpret both edges from long-range markings, cross-sections, and human guidance, separate sidewalks and inferred occlusions, draw into a working copy, and retain actual overlays, correction reasons, and unresolved questions.

Supply source imagery, area/route, human annotations, and tools. Define carriageway, sidewalk, or total paved-area scope. Satellite and orthorectified imagery are the current scenarios; other sources, formats, and registration depend on the tools. No elevation, contour, or survey topographic-map generation is claimed from ordinary 2D imagery.

Expected outputs: editable boundaries, stable IDs, evidence, source/candidate and actual-overlay comparisons, uncertainty, and correction records.

## Optional helpers and validation

`geometry.py` uses the Python standard library for coordinates and constant-width geometry. `evidence_strips.py` requires Pillow 10.1+ and organizes original-coordinate evidence. Neither recognizes roads. References and the audit template live with the self-contained road skill.

```shell
python -m pip install "Pillow>=10.1"
python skills/satellite-road-edge-tracing/scripts/geometry.py --self-test
python skills/satellite-road-edge-tracing/scripts/evidence_strips.py --help
```

This early project has no independent survey truth, cross-region benchmark, or controlled model comparison. Equivalent quality across models/reasoning settings is unproven. Many review steps depend on the agent following the procedure; they are not all enforced by code. Format/helper checks do not establish visual accuracy. See [validation scope](docs/validation.md).

Contribute shareable source → failed candidate → evidence/correction → actual-overlay examples, blind evaluations, adapters, or new domain skills. Explain why a correction was necessary as well as showing the final geometry.

Fork, modify, redistribute, and contribute improvements through issues and pull requests under MIT. 欢迎共享、改进和贡献，遵循MIT许可；见[贡献说明](CONTRIBUTING.md)。

## License

[MIT](LICENSE). External imagery, standards, and tools retain their own licenses.
