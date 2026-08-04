# GoldenEye (1995) — ARKANGEL

*film package · mission codename ARKANGEL*. Mission **ARKANGEL**: model the orbital EMP threat envelope (detonation to ground effects); assess electronics kill radii by vulnerability class; evaluate Arkangel dam-facility security and breach flood risk.

## Concepts

orbital EMP, infrastructure resilience

## Abstract (imported from the package manuscript)

**GoldenEye: ARKANGEL** (film identity **GOLDENEYE**, mission codename **ARKANGEL**) is a deterministic special-agent mission software package that models three coupled threat surfaces from the 1995 film *GoldenEye*: an orbital electromagnetic-pulse (EMP) weapon, the electronics kill-radius it imposes on surface assets, and the security and breach-flood risk of the Arkangel dam facility. The threat envelope is a documented conservative point-source model of a high-altitude nuclear burst (**2000.0** kt at **300.0** km), producing a nadir early-time field of **90125** V/m across a line-of-sight footprint of radius **1978** km (**12291795** km^2). Four electronics vulnerability classes (**4** in total: **unprotected, commercial, military, legacy_tube**) are assessed: unprotected microelectronics are destroyed over essentially the entire visible footprint (**1978.0** km, **100.0**\% of it), while MIL-STD-188-125-hardened and legacy vacuum-tube electronics require ever-higher fields and survive to within **268.7** km of the burst or are immune (**0.0** km). For the Arkangel dam, the report combines the published Froehlich (1995) breach-outflow regression with the Ritter (1892) instantaneous dam-break solution. Given a reservoir of **130000000** m^3 behind a **75.0** m head, peak outflow reaches **31760** m^3/s with a wave front moving at **54.2** m/s; the facility **8.0** km downstream faces a **33.3** m peak inundation within **2.5** min — an overall **extreme** risk. Defense-in-depth access control yields a **0.987** detection probability and a **89.3** composite security score. All results are closed-form, deterministic, and regenerable from source; figures, data, and manuscript variables are produced by thin orchestration scripts under `scripts/`.

## Sources

@glasstone1977effects; @iec6100029; @milstD188125; @froehlich1995peak; @ritter1892fortpflanzung; @stoker1957water

