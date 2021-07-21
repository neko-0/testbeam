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

    channel_pair = [(6, 5)]

    pmax_cuts = [f"pmax_ch{x} > 10" for x in range(8)]
    good_track_events = good_track_events.Filter("||".join(pmax_cuts))

    good_track_events = good_track_events.Filter("pmax_ch6>10")

    sel = RectangleSel("sel", -5.3, -5.25, 9.5, 11.5)
    good_track_events = good_track_events.Filter(sel.root_selection("r_xhit", "r_yhit"))

    buffer = []
    color = 2
    for pair in channel_pair:
        ch1, ch2 = pair

        binning = (f"pmax_tmax{ch1}", f"pmax_tmax{ch2}", 500, 0, 200, 500, 0, 200)
        histo = good_track_events.Histo2D(binning, f"pmax_ch{ch1}", f"pmax_ch{ch2}")
        histo.GetYaxis().SetTitle(f"pmax_ch{ch2}")
        histo.GetXaxis().SetTitle(f"pmax_ch{ch1}")
        histo.SetMarkerColor(color)
        buffer.append(histo)
        color += 1

    opt = ""
    canvas = ROOT.TCanvas(f"canvas_cc", "", 1200, 800)
    canvas.cd()
    for histo in buffer:
        histo.SetMarkerStyle(7)
        histo.SetMarkerSize(10)
        histo.Draw(opt)
        opt = "SAME"
    canvas.SaveAs(f"pmax_ch5_64.png")


if __name__ == "__main__":
    main()
