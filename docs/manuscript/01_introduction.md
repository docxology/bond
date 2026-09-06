# Introduction

PROJECT BOND applies the research template's *forkable project* paradigm at
fleet scale. One source scaffold — `template_code_project` — was clean-copied
into {{N_PACKAGES}} standalone packages, each with its own git repository, its
own identity (`pyproject.toml`, `docs/manuscript/config.yaml`,
`README.md`/`AGENTS.md`/`TODO.md`), and its own `src/` test suite. Every
package meets the same bar: pure, deterministic algorithm cores; zero mock
framework; ≥90% line+branch coverage on `src/`; thin orchestrator scripts; and
manuscript variables injected from configuration.

## Two-layer topology: shared infrastructure and film-specific algorithms

- **Layer 1 · mission infrastructure ({{N_INFRA}} packages).** `bond-utilities`
  (codename Q-BRANCH) provides the shared primitives — ciphers, deterministic
  codenames, mission clocks, seeded randomness, and provenance-aware mission
  records. `bond-api` (THE PROTOCOL) freezes the `MissionProvider` contract —
  `brief` / `recon` / `plan` / `execute` / `debrief` — that every film
  implements, plus a gadget registry and slug-based discovery.
  `bond-coordinator` (MISSION CONTROL) is the fleet registry, mission ledger,
  status, and situation room. `bond-orchestrator` (DAG 00) runs multi-package
  missions in dependency order with checkpoint/resume. `bond-cli` (THE FRONT
  DOOR) is the unified terminal: `bond list` / `brief` / `recon` / `plan` /
  `execute` / `debrief` / `run` / `status` / `gadgets`. `bond-ops`
  (QUARTERMASTER) runs fleet inventory and the aggregate gate.

- **Layer 2 · the films ({{N_FILMS}} packages).** Each film package models the
  operational concepts behind one Bond film — a distinct, real, tested
  algorithm surface: isotope forensics (`dr_no`), underwater/nuclear-security
  planning (`thunderball`), space-mirror targeting geometry
  (`diamonds_are_forever`, `die_another_day`), narcotics-network analytics
  (`live_and_let_die`, `licence_to_kill`), orbital-EMP modeling (`goldeneye`),
  poker game theory (`casino_royale_2006`), cyber operations (`skyfall`),
  surveillance-network analysis (`spectre`), DNA-targeted bioweapon
  countermeasures (`no_time_to_die`), and more. Each implements the frozen
  `MissionProvider` in `src/<slug>/mission.py` and is discoverable by the
  orchestrator.

## Generation, hydration, and provenance of the compendium

Every chapter below is **generated from the corresponding package's own
manuscript**. Each chapter reproduces that package's complete manuscript
rather than an excerpt: the abstract and every authored section are imported,
token- and configuration-hydrated from the package's own manuscript variables,
the package's figures are carried into the combined PDF, and its references
are folded into the unified bibliography. The introduction and the closing are
the only hand-written prose here; the architecture chapter, the full-text
package chapters, the reference list, and the bibliography are produced by
`scripts/generate_compendium.py` and are regenerable on demand.

The following chapters carry the suite's shared foundation, then every film
and infrastructure package in full — abstract, methods, results, conclusion,
reproducibility, and scope — and close with a synthesis of the whole.
