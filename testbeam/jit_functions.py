"""
JIT functions use in RDataFrame Filter and Definition
"""


def unpack_amplitude(wfm_size, channel):
    """
    JIT function that unpack 2D array of amplitude.
    RDataFrame will only flatten 2D array in TTree ATM.
    """
    jit_function = f"""
        std::vector<double> wfm;
        wfm.reserve({wfm_size});
        int start = {channel*wfm_size};
        int end = {(channel+1)*wfm_size};
        for( int p=start; p < end; p++) wfm.push_back(channel[p]);
        return wfm;
    """
    return jit_function


def unpack_time(wfm_size):
    jit_function = f"""
        std::vector<double> t;
        t.reserve({wfm_size});
        for(int p=0; p<{wfm_size}; p++) t.push_back((time[p]-LP2_50[7])*1.0e9);
        return t;
    """
    return jit_function


def rotate(degree, x, y):
    jit_function = f"""
        TRotation r;
        return r.RotateZ({degree}) * TVector3({x},{y},0);
    """
    return jit_function
