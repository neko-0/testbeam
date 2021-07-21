import ROOT
from testbeam import filtering
from testbeam.pad_selection import RectangleSel, CircleSel


def main():
    do_hit_map = True

    ROOT.EnableImplicitMT()

    ROOT.gROOT.SetBatch(True)

    src_dir = "/media/mnt/COVID-19/FNAL_TB_AC_Feb2021/BNL2021_narrow_285V_299/*.root"
    df = ROOT.RDataFrame("pulse", src_dir)

    good_track_events = getattr(filtering, "nominal")(df)

    pad_region = RectangleSel("pad", -5.3, -5.25, 9.5, 11.5)

    exclude_region = RectangleSel("exclude", -5.8, -3, 9, 9.3)

    circle = CircleSel("circle", -5.4, 11, 0.1)

    # create 2D profile of hits
    if do_hit_map:
        binning = (150, -5.8, -4.5, 150, 9, 12, 0, 500)
        pmax_profiles = []
        for i in range(0, 7):
            hist_info = (f"channel{i}", f"channel{i}", *binning)
            profile = good_track_events.Profile2D(
                hist_info, "r_xhit", "r_yhit", f"pmax_ch{i}"
            )
            profile.GetYaxis().SetTitle(f"yhit")
            profile.GetXaxis().SetTitle(f"xhit")
            pmax_profiles.append(profile)

        for i, histo in enumerate(pmax_profiles):
            canvas = ROOT.TCanvas(f"canvas{i}", "", 1200, 800)
            canvas.cd()
            histo.Draw("colz")
            pad_region.root_draw()
            exclude_region.root_draw()
            circle.root_draw()
            canvas.SaveAs(f"hit_pmax{i}.png")

    for evt in range(100000):
        pmax_threshold = [0]#, 15, 30, 50, 100, 150, 250]
        for threshold in pmax_threshold:
            buffer = []
            # filter with pmax threshold and create signal sum columns
            threshold_cuts = [
                f"pmax_ch0 > {threshold}",
                f"pmax_ch1 > {threshold}",
                f"pmax_ch2 > {threshold}",
                f"pmax_ch3 > {threshold}",
                f"pmax_ch4 > {threshold}",
                f"pmax_ch5 > {threshold}",
                f"pmax_ch6 > {threshold}",
            ]
            high_pmax_df = good_track_events.Filter("||".join(threshold_cuts))

            for ch in [0,6]:
                pad_signal_df = high_pmax_df.Filter(f"pmax_ch{ch}>{threshold}")
                pad_signal_df = pad_signal_df.Filter(f"{pad_region.root_selection('r_xhit', 'r_yhit')}")
                pad_signal_df = pad_signal_df.Filter(f"i_evt == {evt}")
                bins = (f"{threshold}{ch}", "", 200, -20, 10, 200, -500, 100)
                waveform = pad_signal_df.Histo2D(bins, "time_ns", f"wfm_ch{ch}")
                buffer.append(waveform)
            print(f"finish {threshold}")

            legend = ROOT.TLegend(0.2, 0.2, 0.35, 0.35)
            legend.SetHeader(f"location {pad_region.vertex()}")

            canvas = ROOT.TCanvas(f"{threshold}{evt}", "", 1200, 800)
            canvas.cd()
            draw_opt = ""
            for color, g in enumerate(buffer, start=2):
                g.GetYaxis().SetRangeUser(-20, 20)
                g.GetXaxis().SetTitle("time")
                g.GetYaxis().SetTitle("amplitude")
                g.SetLineColor(color)
                g.SetMarkerSize(2)
                g.SetMarkerStyle(8)
                g.SetMarkerColor(color)
                g.SetLineWidth(2)
                g.Draw(draw_opt)
                draw_opt = "same"
                canvas.Update()
                legend.AddEntry(g.GetValue(), f"strip-{color-2}")
            print("done")
            legend.Draw()
            canvas.SaveAs(
                f"hit_{'_'.join([str(x) for x in pad_region.vertex()])}_strips_waveform_threshold{threshold}_up5_{evt}.png"
            )


if __name__ == "__main__":
    main()
