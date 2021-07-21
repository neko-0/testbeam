import ROOT
from testbeam import filtering
from testbeam.pad_selection import PadRegion


if __name__ == "__main__":

    do_hit_map = False

    ROOT.EnableImplicitMT()

    ROOT.gROOT.SetBatch(True)

    src_dir = "../BNL2021_narrow_285V_299/*.root"
    df = ROOT.RDataFrame("pulse", src_dir)

    good_events = getattr(filtering, "nominal")(df)

    # create 2D profile of hits
    if do_hit_map:
        binning = (150, -5.8, -4.5, 150, 9, 12, 0, 500)
        pmax_profiles = []
        for i in range(0, 7):
            hist_info = (f"channel{i}", f"channel{i}", *binning)
            profile = good_track_events.Profile2D(
                hist_info, "xhit", "yhit", f"pmax_ch{i}"
            )
            profile.GetYaxis().SetTitle(f"y [um]")
            profile.GetXaxis().SetTitle(f"x [um]")
            pmax_profiles.append(profile)

        for i, histo in enumerate(pmax_profiles):
            canvas = ROOT.TCanvas(f"canvas{i}", "", 1200, 800)
            canvas.cd()
            histo.Draw("colz")
            canvas.SaveAs(f"hit_pmax{i}.png")
