# Never Say Never Again (1983) — REPLAY

*film package · mission codename REPLAY*. Mission **REMOUNT**: replay the legacy operation as a remount; diff the original vs remount outcomes; migrate the legacy intelligence assets; assess remount detection risk and mission reliability; allocate remastered assets by marginal gain; forecast the replay learning curve.

## Concepts

legacy remount, replay

## Abstract (imported from the package manuscript)

**Never Say Never Again: REMOUNT — Special-Agent Mission Software** (Legacy mission replay, op diff, and remastered-intel migration, version 0.1.0) presents REMOUNT, a deterministic engine for *legacy mission replay*. When an operation is re-opened years after its original run, its scenario must be re-executed — as a *remount* — with remastered intelligence, its outcomes compared against the original, and its legacy assets migrated so they can be consumed safely again. Drawing on the 1983 film *Never Say Never Again* — itself a remount of the 1965 *Thunderball* operation (Never Say Never Again, mission codename REMOUNT) — the engine models each of 4 objectives through a smooth success curve over effective intel versus difficulty. The canonical replay yields an original command score of 0.3111 and a remount command score of 0.5161 (weighted delta +0.2050, overall verdict *improved*). Per-objective, the remount improves 4 objectives, regresses 0, and leaves 0 unchanged. The engine migrates 4 legacy intelligence dossiers, re-fingerprinting each (SHA-256) so the remount can verify integrity before consumption (fingerprint e8e4301892e4). The remount is not costless. Replaying the op accumulates a detection hazard: over a campaign of replay operations the probability of alerting the adversary reaches 0.7769 (expected 4.00 operations before alert), while the mission's block-structured reliability is 0.9578 — a campaign expected value of +18.10. Scarce remastered assets are therefore allocated by marginal gain (6 assets deployed, 0.7804 of the saturation ceiling), and repeated rehearsal pushes the command score along an exponential learning curve toward 0.7010 (delta +0.3899, reaching the target by iteration 3). Everything computes deterministically — no random draws, no external calls — so the remount is reproducible to the byte on Python 3.14.6 (generated 2026-08-05T00:11:18+00:00).

## Sources

@bond_api; @bond_utilities; @nemhauser1978submodular; @wright1936learning; @barlow1975reliability

