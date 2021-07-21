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

    pmax_cuts = [f"pmax_ch{x} > 0" for x in range(8)]
    good_track_events = good_track_events.Filter("&&".join(pmax_cuts))

    good_track_events = good_track_events.Filter("pmax_ch6>0")
    # good_track_events = good_track_events.Filter("corr_tmax_ch6>-10.6 && corr_tmax_ch6<-9.6")
    sel = RectangleSel("sel", -5.3, -5.25, 9.5, 11.5)
    #good_track_events = good_track_events.Filter(sel.root_selection("r_xhit", "r_yhit"))

    histo_buffer = []
    for i in range(nchannel):
        binning = (f"pmax_tmax{i}", f"pmax_tmax{i}", 500, -100, 100, 350, -11, -9)
        histo = good_track_events.Histo2D(binning, f"pmax_ch{i}", f"corr_tmax_ch{i}")
        histo.GetYaxis().SetTitle(f"tmax{i}-cfd7[20]")
        histo.GetXaxis().SetTitle(f"pmax{i}")
        histo_buffer.append(histo)

    for i, histo in enumerate(histo_buffer):
        canvas = ROOT.TCanvas(f"canvas{i}", "", 1200, 800)
        canvas.cd()
        histo.SetMarkerStyle(7)
        histo.SetMarkerSize(10)
        histo.Draw()
        canvas.SaveAs(f"pmax_tmax{i}.png")


if __name__ == "__main__":
    main()
