# Expts descriptions and detailed configurations.

## Testing availability of HadCM3 using old data

A set of experiments were carried out following the configurations of Chris' `xpza`.  

## xqcha

This is a straight copy from `xpuoo` (for testing purposes).  

## xqchb

Copied from `xpzab`, control run of `xpza`.  The GHGs in `xqchb` are not updated from [SRES data](https://www.ipcc.ch/site/assets/uploads/2018/03/sres-en.pdf) (Special Report on Emissions Scenarios, very likely).
> `xpzab`: Spin-up ii. Dynamic TRIFFID. 200 years to finish spin-up. After this check veg frac, carbon stores and ocean fluxes are in steady state. Copy from `xpzaa`, but turn to dyn triffid (10-day period), and edit a few diags. TRIFFID profile set to 480 timesteps. **Plan to leave this going as a control run, and start point for subsequent runs.**
>
>> `xpzaa`: Spin-up, equilibrium TRIFFID. 40 years, 8*5 TRIF periods. Copy from `xpwca`, but largely doesn't matter. Can go from any start dump. Differences below are from Paul's `tfita`.
>>
>>> `tfita`: UTOPIA advection on all tracers. This is near final retuning setup. Tuned surface NPP and deep ocean oxygen. This uses remin_temp_depend_05a. run for 3000 years.
>>
>> 1. Needs mods:
>>
>>- `/user/home/tw23150/mods/gath_fld_co2.mf77`:CO<sub>2</sub> passing in gather field is on different grid as it's a diagnostic. *Not necessarily needed for conc-driven runs, but good practice to include all the time so not forgotten.*
>>
>>- `$PV_UPDATES/znamelist_hadcm3m21_land_cc.mod`: remove this MOD, and remove this local post-proc script: `~ggpjv/scripts/land_cc`.
>>
>> 2. Tracers:
>>
>>- Turn on tracers in the atmosphere (`Atmosphere`->`Model Configuration`->`Tracers`), and select ozone (we don't use it, but the model crashed if none were selected). We'll need this for CO<sub>2</sub> as a tracer so that the code is included.
>>
>>- In (`Atmosphere`->`Scientific Parameters and Sections`->`Section by section choices`->`Atmospheric tracer advection`), select `1A> Atmospheric tracer advection included`, but keep `experimental thetal and qt advection` turned off.
>>
>> 3. TRIF eqbm mode:
>>
>>- Phenol (leaf phenology) on, 1 day period
>>- TRIF eqbm, 1800 day period (5 years)
>>- Provide land-use/disturbance file: `qrfrac.disturb.H3Bris.anc`
>>- Check stash profile for a few veg diags:
>>    - TRIFFID time profile is instantaneous ourput every 86400 timesteps
>>
>> 4. CO<sub>2</sub>:
>>
>>    Check CO<sub>2</sub> is 4.25418e-04 (280 ppm) – this gets hardwired later, so important for spin-up. Set 280 ppm in ocean carbon cycle panels. There's no current way to check for internal consistency – **so need to keep in mind doing this manually...**
>>
>> 5. Ocean:
>>
>>    No changes to ocean panels from Paul's job.


## xqchc

Copy from `xqchb`, we changed the GHGs conc here from the latest CMIP6 dataset ([input4MIPs](https://docs.google.com/document/d/1pU9IiJvPJwRvIgVaSDdJ4O0Jeorv_2ekEtted34K9cA/edit?tab=t.0#heading=h.kbcgohrf04fo)), for methane, nitrous oxide, CHC12-eq and HFC134A-eq for 7 periods from 1850–2014.

## xqchd

Copy from `xqchb`, we changed both the GHGs conc here as well as the CO<sub>2</sub> conc, similarly to xqchc.

## xqche

Copy from `xqchb`, here we do not consider the conc of GHGs other than CO<sub>2</sub>, so put them at default values.  
For CO<sub>2</sub> emit, two things need to be done:

1. Turn on the tracers to allow the interaction between the atmos and the ocean
2. Provide emission ancillary file to allow the convection/calc  

This simulation runs from 1650 to 1850, without emission ancil files provided (start from 280 ppmv).  
To do this (emission driven), we need to:

1. Have tracers on – this is already done above, but from here it is needed.
2. Select CO<sub>2</sub> `from interactive carbon cycle` and set a constant value to initialise (unless we want to run from an existing dump). Use same as would be prescribed: 4.25418e-04. For spin-up we don't want emisssions, so select that as `not-used`.
3. To make sure the right prognostics are initialised, we need the following in the `RECONA`/`RECONO` files:  
   - `RECONA`  

    `### Tracer fields ###`  
    `&ITEMS ITEM=61, DOMAIN=1, SOURCE=6, USER_PROG_RCONST=1.0000e-06 &END`  
    `### Co2 Field for interactive carbon cycle ###`  
    `&ITEMS ITEM=250, DOMAIN=1, SOURCE=6, USER_PROG_RCONST=0.0e-00 &END`  
    `&ITEMS ITEM=251, DOMAIN=1, SOURCE=6, USER_PROG_RCONST=0.0e-00 &END`  
    `&ITEMS ITEM=252, DOMAIN=1, SOURCE=6, USER_PROG_RCONST=4.25418e-04 &END`  
    
    > The tracer is required or else the tracer code doesnot run. We don't actually use it. For the CO<sub>2</sub> fields, 250 is the ocean flux – initialise this to zero or else there is no data on the first day. After day 1 it gets passed in from the ocean. 251 is the emissions  – again set to zero unless we want to run with a specified emission or read in from file. 252 is the CO<sub>2</sub> conc itself in MMR. This line should already be there, and set to the value we chose in the umui.
    >
   - `RECONO`  

    `&ITEMS ITEM=200, DOMAIN=1, SOURCE=6, USER_PROG_RCONST=280.0e-00 &END`  

    > This sets the atmos CO<sub>2</sub> – again will get passed by the model once it is running, but good to set here for a sensible start value.  
    > 
4. Need CO<sub>2</sub> diags for stash and coupling
   - `Atmos STASH`  
    We have to set this up to pass the surface level CO<sub>2</sub> conc to the ocean. To do this, we need to add CO<sub>2</sub> 3D tracer (sec 0, item 251) with the following profiles:
        - `TDAYMN`: to give daily mean (will likely already exist)  
        - `DA1`: just passes in bollom level. May or may not exist, select `full levels`, `:range of levels` then `start` and `end` both set to 1.  
        - `UPA2O`: will likely need creating if we're not starting from a c-cycle job. Select `dump store with user specified TAG` and set the TAG to 10.  
    Note – this is just to enable the passing of the variable to the ocean. The run will fail without this, but this doesn't give any output. If we want to output the CO<sub>2</sub> then we need to duplicate this diag, but set it to output to a normal ourput profile/pp file.  
   - `Ocean STASH`  
    We have to set this up to pass the ocean flux of CO<sub>2</sub> to the atmosphere. To do this, we need to add CO<sub>2</sub> flux (sec 30, item 249) – this is quite likely already there, but we'll need a duplicate entry for the coupling as per the CO<sub>2</sub> above. Set this with the following profiles:
        - `TDAYMN`: daily mean  
        - `DIAG`: surface field  
        - `UPO2A`: the converse of `UPA2O` above. Set this for a user specified TAG of 11.  
    (aside – when starting a coupled run the first day of atmosphere has no ocean flux, so it may be missing data for day 1 – this can screw up disgnostics – e.g., our monthly or annual mean might look crazy – but the model itself will zero it out and not actually apply MDI (What is this?:confused:) as a flux).  

## xqchf

Basically copy of `xqche`, some differences are:  

1. We used an ancillary file of CO<sub>2</sub> emissions from 1750 to 2100 rather than input a constant conc value.  

2. As ancil data start from 1750, we changed the model basis time from 1650 to 1750 and running length to be 350 model years.
   > 
   > Emissions file produced by Alex, data from Chris.  
  
## xqcht

