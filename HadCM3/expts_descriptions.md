# Expts descriptions and detailed configurations.

## Testing availability of HadCM3 using old data

A set of experiments were carried out following the configurations of Chris' xpza.  

- xqcha

This is a straight copy from xpuoo (for testing purposes).  

- xqchb

Copied from xpzab, control run of `xpza`.  The GHGs in `xqchb` are not updated from [SRES data](https://www.ipcc.ch/site/assets/uploads/2018/03/sres-en.pdf) (Special Report on Emissions Scenarios, very likely).
> `xpzab`: Spin-up ii. Dynamic TRIFFID. 200 years to finish spin-up. After this check veg frac, carbon stores and ocean fluxes are in steady state. Copy from xpzaa, but turn to dyn triffid (10-day period), and edit a few diags. TRIFFID profile set to 480 timesteps. **Plan to leave this going as a control run, and start point for subsequent runs.**
>
>> `xpzaa`: Spin-up, equilibrium TRIFFID. 40 years, 8*5 TRIF periods. Copy from xpwca, but largely doesn't matter. Can go from any start dump. Differences below are from Paul's tfita.
>>
>>> `tfita`: UTOPIA advection on all tracers. This is near final retuning setup. Tuned surface NPP and deep ocean oxygen. This uses remin_temp_depend_05a. run for 3000 years.
>>
>> 1. Needs mods:
>>
>>    - `/user/home/tw23150/mods/gath_fld_co2.mf77`:CO<sub>2</sub> passing in gather field is on different grid as it's a diagnostic. Not necessarily needed for conc-driven runs, but good practice to include all the time so not forgotten.
>>
>>    - `$PV_UPDATES/znamelist_hadcm3m21_land_cc.mod`: remove this MOD, and remove this local post-proc script: `~ggpjv/scripts/land_cc`.
>>
>> 2. Tracers:
>>
>>    - Turn on tracers in the atmosphere (`Atmosphere`->`Model Configuration`->`Tracers`), and select ozone (we don't use it, but the model crashed if none were selected). We'll need this for CO<sub>2</sub> as a tracer so that the code is included.
>>
>>    - In (`Atmosphere`->`Scientific Parameters and Sections`->`Section by section choices`->`Atmospheric tracer advection`), select `1A> Atmospheric tracer advection included`, but keep `experimental thetal and qt advection` turned off.
>>
>> 3. TRIF eqbm mode:
>>
>>    - Phenol (leaf phenology) on, 1 day period
>>    - TRIF eqbm, 1800 day period (5 years)
>>    - Provide land-use/disturbance file: qrfrac.disturb.H3Bris.anc
>>    - Check stash profile for a few veg diags:
>>      - TRIFFID time profile is instantaneous ourput every 86400 timesteps
>>
>> 4. CO<sub>2</sub>:
>>
>>    Check CO<sub>2</sub> is 4.25418e-04 (280 ppm) – this gets hardwired later, so important for spin-up. Set 280 ppm in ocean carbon cycle panels. There's no current way to check for internal consistency – **so need to keep in mind doing this manually...**
>>
>> 5. Ocean:
>>
>>    No changes to ocean panels from Paul's job.


- xqchc

Copy from `xqchb`, we changed the GHGs conc here from the latest CMIP6 dataset ([input4MIPs](https://docs.google.com/document/d/1pU9IiJvPJwRvIgVaSDdJ4O0Jeorv_2ekEtted34K9cA/edit?tab=t.0#heading=h.kbcgohrf04fo)), for methane, nitrous oxide, CHC12-eq and HFC134A-eq for 7 periods from 1850–2014.

- xqchd

Copy from xqchb, we changed both the GHGs conc here as well as the CO<sub>2</sub> conc, similarly to xqchc.

- xqche

Copy from xqchb, here we do not consider the conc of GHGs other than CO<sub>2</sub>, so put them at default values.  
For CO<sub>2</sub> emit, two things need to be done:

    - Turn on the tracers to allow the interaction between the atmos and the ocean
    - Provide emission ancillary file to allow the convection/calc  
This simulation runs from 1650 to 1850, without emission ancil files provided (start from 280 ppmv).  

- xqchf

Basically copy of xqche, some differences are:  
    - We used an ancillary file of CO<sub>2</sub> emissions from 1750 to 2100 rather than input a constant conc value.
    - As ancil data start from 1750, we changed the model basis time from 1650 to 1750 and running length to be 350 model years.
- > Emissions file produced by Alex, data from Chris.
- xqcht

