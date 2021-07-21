import ROOT
from testbeam import filtering
from testbeam.pad_selection import RectangleSel, CircleSel


def main():

    ROOT.EnableImplicitMT()

    ROOT.gROOT.SetBatch(True)

    src_dir = "/media/mnt/COVID-19/FNAL_TB_AC_Feb2021/BNL2021_narrow_285V_299/*.root"
    df = ROOT.RDataFrame("pulse", src_dir)

    good_track_events = getattr(filtering, "nominal")(df)

    nchannel = 8

    channel_pair = [(6, 1)]

    pmax_cuts = [f"pmax_ch{x} > 10" for x in range(8)]
    good_track_events = good_track_events.Filter("||".join(pmax_cuts))

    good_track_events = good_track_events.Filter("pmax_ch6>50")

    sel = RectangleSel("sel", -5.3, -5.25, 9.5, 11.5)
    good_track_events = good_track_events.Filter(sel.root_selection("r_xhit", "r_yhit"))

    # convert to numpy array
    # my_array = good_track_events.AsNumpy(columns=["pmax_ch1", "pmax_ch2"]) -> dict(np.array)

    buffer = []
    color = 2
    for i in range(1, 7):
        binning = (f"pmax_tmax_ch{i}", f"pmax_tmax_ch{i}", 500, -100, 500)
        histo = good_track_events.Histo1D(binning, f"pmax_ch{i}")
        histo.SetLineColor(color)
        buffer.append(histo)
        color += 1

    canvas = ROOT.TCanvas(f"canvas_cc", "", 1200, 800)
    leg = ROOT.TLegend()
    canvas.cd()
    opt = ""
    for i, histo in enumerate(buffer, start=1):
        # histo.SetMarkerStyle(7)
        # histo.SetMarkerSize(10)
        histo.GetYaxis().SetRangeUser(0, 500)
        histo.Draw(opt)
        leg.AddEntry(histo.GetValue(), f"ch{i}")
        opt = "SAME"
    leg.Draw()
    canvas.SetLogx()
    canvas.SaveAs(f"pmax1D_ch5_64.png")


if __name__ == "__main__":
    main()
