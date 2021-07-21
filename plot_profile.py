import ROOT
from testbeam import filtering
from testbeam.pad_selection import RectangleSel, CircleSel

if __name__ == "__main__":

    do_hit_map = False

    ROOT.EnableImplicitMT()

    ROOT.gROOT.SetBatch(True)

    ROOT.gStyle.SetOptStat(0)

    src_dir = "../BNL2021_narrow_285V_299/*.root"
    df = ROOT.RDataFrame("pulse", src_dir)

    # applying nominal filtering
    good_events = getattr(filtering, "nominal")(df)

    # booking profile plots
    xy_bin = (150, -5.8, -4.5, 150, 9, 12)
    booking = {
        "pmax": {"zrange": (-100, 500), "obs": "pmax_ch{}"},
        "noise": {"zrange": (-5, 5), "obs": "noise_ch{}"},
        "rise_time": {"zrange": (-800, 0), "obs": "risetime_ch{}"},
    }

    circle = CircleSel("circle", -5.4, 10.5, 0.05)

    buffer = {}
    for key in booking:
        buffer[key] = []
        for i in range(0, 7):
            bin = (*xy_bin, *booking[key]["zrange"])
            obs = booking[key]["obs"].format(i)
            histo_bin = (f"{key}_ch{i}", f"{key}_ch{i}", *bin)
            profile = good_events.Profile2D(histo_bin, "r_xhit", "r_yhit", obs)
            profile.GetYaxis().SetTitle(f"y [um]")
            profile.GetXaxis().SetTitle(f"x [um]")
            profile.GetZaxis().SetRangeUser(*booking[key]["zrange"])
            buffer[key].append(profile)

    for key in buffer:
        for i, histo in enumerate(buffer[key]):
            canvas = ROOT.TCanvas(f"{key}_canvas{i}", "", 1200, 800)
            canvas.SetRightMargin(0.15)
            canvas.cd()
            histo.Draw("colz")
            circle.root_draw()
            canvas.SaveAs(f"hit_{key}{i}.png")
