# Skill discovery and installation / 技能检索与安装

Project: **Agentic Map Tracing**. Repository: [capskov/agentic-map-tracing](https://github.com/capskov/agentic-map-tracing). Release: **v0.1.0-beta.1**. Skill: **satellite-road-edge-tracing**.

Read [AGENTS.md](../AGENTS.md), then load [SKILL.md](../skills/satellite-road-edge-tracing/SKILL.md) for satellite/aerial pavement edges, occluded junctions, lane/cross-section interpretation, human guidance or repeated CAD/GIS overlay offsets. The agent decides where a boundary belongs and why; helpers do not recognize roads.

Copy the complete `skills/satellite-road-edge-tracing` folder to the host skill directory. Codex commonly uses `~/.codex/skills/`. Frontmatter supports skill discovery; `agents/openai.yaml` supplies compatible host UI metadata. The skill folder includes its own MIT license.

With the [Skills CLI](https://skills.sh/docs/cli):

```shell
npx skills add capskov/agentic-map-tracing --skill satellite-road-edge-tracing
```

Invoke `$satellite-road-edge-tracing` with original imagery, scope, route, human references and actual CAD/GIS tools. Format support does not certify every host.

This is a standard SKILL.md package, not official OpenAI approval or guaranteed directory indexing. `skill-catalog.json` is this project's navigation catalog, not an official universal registry. `llms.txt` is a navigation aid. Separate [CAD Agent Foundation](https://github.com/capskov/cad-agent-foundation) is the MCP/CLI backend; its registration is independent. Neither component installs the other or grants drawing access.

Keywords: Agent Skill, geospatial visual reasoning, satellite road-edge tracing, aerial imagery digitization, pavement boundaries, paired road bands, lane markings, cross-sections, occlusion, channelization, human feedback, editable CAD/GIS, overlay review, 卫星图判读、道路边线、人工示教、整体偏移纠错。
