import ROOT

ROOT.gROOT.SetBatch(True)


def pmax_tmax(file, nchannel=8):

    dframe = ROOT.RDataFrame("pulse", file)

    binning = (100, 0, 200, 100, 1, 1)

    histo_buffer = []
    for i in range(nchannel):
        histo = dframe.Histo2D(
            (f"pmax_tmax{i}", f"pmax_tmax{i}", *binning), f"amp[{i}]", f"t_peak[{i}]"
        )
        histo.GetYaxis().SetTitle(f"tmax{i}")
        histo.GetXaxis().SetTitle(f"pmax{i}")
        # import pdb; pdb.set_trace()
        histo_buffer.append(histo)

    for i, histo in enumerate(histo_buffer):
        canvas = ROOT.TCanvas(f"canvas{i}", "", 1200, 800)
        canvas.cd()
        histo.SetMarkerStyle(7)
        histo.SetMarkerSize(10)
        histo.Draw()
        canvas.SaveAs(f"pmax_tmax{i}.png")


def hits(file, nchannel=8):

    dframe = ROOT.RDataFrame("wfm", file)
    binning = (50, -8, -3, 50, 8, 12, 0, 500)

    histo_buffer = []
    for i in range(nchannel):
        filter = f"pmax{i} > 10 && passBaselineCut"
        histo = dframe.Filter(filter).Profile2D(
            (f"hits{i}", f"hits{i}", *binning), "x_dut", "y_dut", f"pmax{i}"
        )
        histo.GetYaxis().SetTitle(f"y_dut{i}")
        histo.GetXaxis().SetTitle(f"x_dut{i}")
        histo_buffer.append(histo)

    for i, histo in enumerate(histo_buffer):
        canvas = ROOT.TCanvas(f"canvas{i}", "", 1200, 800)
        canvas.cd()
        histo.Draw("colz")
        canvas.SaveAs(f"hit_pmax{i}.png")


def plot_histo1D(file, observables=["pmax", "rise", "noise"], nchannel=8):

    dframe = ROOT.RDataFrame("wfm", file)
    binning = (100, 1, 1)

    histo_buffer = {}
    for obs in observables:
        for i in range(nchannel):
            filter = f"pmax{i} > 10 && passBaselineCut"
            histo = dframe.Filter(filter).Histo1D((f"{obs}{i}", *binning), f"{obs}{i}")
            histo.GetYaxis().SetTitle(f"Number of event")
            histo.GetXaxis().SetTitle(f"{obs}{i}")
            histo_buffer[f"{obs}{i}"] = histo

    for i, obs in enumerate(histo_buffer):
        canvas = ROOT.TCanvas(f"canvas{obs}{i}", "", 1200, 800)
        canvas.cd()
        histo_buffer[obs].Draw("HIST")
        canvas.SaveAs(f"{obs}{i}.png")


if __name__ == "__main__":

    tfile = ROOT.TFile.Open("HPK_pad_C2_180V_282.root")

    pmax_tmax(tfile)

    # hits(tfile)

    # plot_histo1D(tfile)
