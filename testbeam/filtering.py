from .jit_functions import unpack_time, unpack_amplitude, rotate


def nominal(df: "ROOT.RDataFrame", degree=-0.9 * 3.14 / 180):
    """
    Nominal selection and observable definition
    """
    track_cleaning_cuts = "ntracks==1 && npix > 0 && nplanes>10 && chi2<30"
    good_track_events = df.Filter(track_cleaning_cuts)

    # list of definition to convert vector/array structure
    # to flat variable in the TTree
    wfm_size = 502
    list_of_definition = []
    list_of_definition.append(("xhit", "x_dut[0]"))
    list_of_definition.append(("yhit", "y_dut[0]"))
    for i in range(8):
        list_of_definition.append((f"pmax_ch{i}", f"amp[{i}]"))
        list_of_definition.append((f"noise_ch{i}", f"noise[{i}]"))
        list_of_definition.append((f"risetime_ch{i}", f"risetime[{i}]*1e-9"))
        list_of_definition.append((f"tmax_ch{i}", f"t_peak[{i}]"))
        # correction tmax with respect to the trigger CFD 20
        list_of_definition.append((f"corr_tmax_ch{i}", f"(t_peak[{i}]-LP2_50[7])*1e9"))
        list_of_definition.append((f"wfm_ch{i}", unpack_amplitude(wfm_size, i)))
    list_of_definition.append(("time_ns", unpack_time(wfm_size)))
    list_of_definition.append(
        ("pmax_sum", "pmax_ch3+pmax_ch4+pmax_ch2+pmax_ch1+pmax_ch5+pmax_ch6")
    )

    for definition in list_of_definition:
        good_track_events = good_track_events.Define(*definition)

    # filtering last channel pmax tmax (track trigger sensor?)
    trigger_cut_string = "pmax_ch7 > 100 && pmax_ch7 < 350 && corr_tmax_ch7 < 0.35"
    good_track_events = good_track_events.Filter(trigger_cut_string)

    # cut out saturation events using pmax
    pmax_cuts = "&&".join([f"pmax_ch{x} < 350" for x in range(8)])
    good_track_events = good_track_events.Filter(pmax_cuts)

    x_mean = good_track_events.Mean("xhit").GetValue()
    y_mean = good_track_events.Mean("yhit").GetValue()

    good_track_events = good_track_events.Define(
        "rotated_vec",
        rotate(degree, f"x_dut[0]-({x_mean})", f"y_dut[0]-({y_mean})"),
    )
    good_track_events = good_track_events.Define(
        "r_xhit", f"rotated_vec.X()+({x_mean})"
    )
    good_track_events = good_track_events.Define(
        "r_yhit", f"rotated_vec.Y()+({y_mean})"
    )

    return good_track_events
