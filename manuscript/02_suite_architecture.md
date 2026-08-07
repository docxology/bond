# Suite Architecture — layered topology, package roster, and measured gate

PROJECT BOND is a 33-package fleet: 27 film packages, each a standalone
software package implementing its film's concepts, plus 6 mission-
infrastructure packages that provide the contract and the operation.

## Layered topology and execution responsibilities

| Layer | Packages |
| --- | --- |
| Layer 0 · utilities | `bond-utilities` (Q-Branch primitives) |
| Layer 1 · protocol | `bond-api` (the frozen MissionProvider contract) |
| Layer 2 · control | `bond-coordinator` (registry, ledger, situation room) |
| Layer 3 · orchestration | `bond-orchestrator` (mission DAG runner, real-film binding) |
| Layer 4 · ops | `bond-cli` (front door), `bond-ops` (fleet gates) |
| Films | 27 standalone packages, one per James Bond film |

Every film implements the frozen `bond_api` `MissionProvider` and is
discovered by `bond_api.discovery`. The compendium imports one chapter per
package below.

## Complete package roster and mission codenames

| # | Package | Codename |
|---|---------|----------|
| 1 | `dr_no` — Dr. No (1962) | CRAB KEY |
| 2 | `from_russia_with_love` — From Russia with Love (1963) | LEKTOR |
| 3 | `goldfinger` — Goldfinger (1964) | GRAND SLAM |
| 4 | `thunderball` — Thunderball (1965) | THUNDERBALL |
| 5 | `you_only_live_twice` — You Only Live Twice (1967) | BIRD ONE |
| 6 | `on_her_majestys_secret_service` — On Her Majesty's Secret Service (1969) | BEDLAM |
| 7 | `diamonds_are_forever` — Diamonds Are Forever (1971) | DIAMOND NET |
| 8 | `live_and_let_die` — Live and Let Die (1973) | SAN MONIQUE |
| 9 | `the_man_with_the_golden_gun` — The Man with the Golden Gun (1974) | SOLEX |
| 10 | `the_spy_who_loved_me` — The Spy Who Loved Me (1977) | LIPARUS |
| 11 | `moonraker` — Moonraker (1979) | MOONRAKER |
| 12 | `for_your_eyes_only` — For Your Eyes Only (1981) | ATAC |
| 13 | `octopussy` — Octopussy (1983) | FABERGE |
| 14 | `a_view_to_a_kill` — A View to a Kill (1985) | MAIN STRIKE |
| 15 | `the_living_daylights` — The Living Daylights (1987) | LIVING DAYLIGHTS |
| 16 | `licence_to_kill` — Licence to Kill (1989) | WAVEKREST |
| 17 | `goldeneye` — GoldenEye (1995) | ARKANGEL |
| 18 | `tomorrow_never_dies` — Tomorrow Never Dies (1997) | CARVER |
| 19 | `the_world_is_not_enough` — The World Is Not Enough (1999) | ELEKTRA |
| 20 | `die_another_day` — Die Another Day (2002) | ICARUS |
| 21 | `casino_royale_2006` — Casino Royale (2006) | LE CHIFFRE |
| 22 | `quantum_of_solace` — Quantum of Solace (2008) | QUANTUM |
| 23 | `skyfall` — Skyfall (2012) | SKYFALL |
| 24 | `spectre` — Spectre (2015) | NINE EYES |
| 25 | `no_time_to_die` — No Time to Die (2021) | HERACLES |
| 26 | `casino_royale_1967` — Casino Royale (1967) | FIVE BONDS |
| 27 | `never_say_never_again` — Never Say Never Again (1983) | REPLAY |
| 28 | `bond-utilities` — Bond Utilities | Q-BRANCH |
| 29 | `bond-api` — Bond API | THE PROTOCOL |
| 30 | `bond-coordinator` — Bond Coordinator | MISSION CONTROL |
| 31 | `bond-orchestrator` — Bond Orchestrator | DAG 00 |
| 32 | `bond-cli` — Bond CLI | THE FRONT DOOR |
| 33 | `bond-ops` — Bond Operations | QUARTERMASTER |

## Aggregate quality gate and coverage evidence

| Package | Coverage |
| --- | --- |
| `dr_no` | 99.0% |
| `from_russia_with_love` | 99.2% |
| `goldfinger` | 100.0% |
| `thunderball` | 100.0% |
| `you_only_live_twice` | 98.0% |
| `on_her_majestys_secret_service` | 98.2% |
| `diamonds_are_forever` | 100.0% |
| `live_and_let_die` | 97.9% |
| `the_man_with_the_golden_gun` | 100.0% |
| `the_spy_who_loved_me` | 100.0% |
| `moonraker` | 99.9% |
| `for_your_eyes_only` | 100.0% |
| `octopussy` | 97.4% |
| `a_view_to_a_kill` | 99.2% |
| `the_living_daylights` | 99.4% |
| `licence_to_kill` | 100.0% |
| `goldeneye` | 99.7% |
| `tomorrow_never_dies` | 98.8% |
| `the_world_is_not_enough` | 99.4% |
| `die_another_day` | 100.0% |
| `casino_royale_2006` | 97.2% |
| `quantum_of_solace` | 100.0% |
| `skyfall` | 100.0% |
| `spectre` | 100.0% |
| `no_time_to_die` | 100.0% |
| `casino_royale_1967` | 100.0% |
| `never_say_never_again` | 100.0% |
| `bond-utilities` | 100.0% |
| `bond-api` | 100.0% |
| `bond-coordinator` | 100.0% |
| `bond-orchestrator` | 99.0% |
| `bond-cli` | 100.0% |
| `bond-ops` | 100.0% |

