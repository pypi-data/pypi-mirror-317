
import matplotlib.pyplot as plt
import numpy as np
import utils

def set_fontsize(font_size=12):
    '''Set font size for all text elements'''
    plt.rcParams['font.size'] = font_size
    plt.rcParams['axes.autolimit_mode'] = 'data' # default: 'data'
    params = {'legend.fontsize': font_size,  # set for all kinds of text elements
            'axes.labelsize': font_size,
            'axes.titlesize': font_size,
            'xtick.labelsize': font_size,
            'ytick.labelsize': font_size}
    plt.rcParams.update(params)
    print(f'Font size is set to {font_size}')

def two_digit_sci_not(x):
    '''Convert a float to a string in scientific notation with 2 digits in the exponent and no decimals.'''
    sci_not_spars = np.format_float_scientific(x, precision=1)
    ## If precision=1, then it's either ceil or exactly precision=0
    if sci_not_spars[2] == 'e':  # exactly precision=0 so one shorter
        sci_not_spars = sci_not_spars[0] + sci_not_spars[2:]  # skip dot
    elif sci_not_spars[3] == 'e':  # ceil
        sci_not_spars = str(int(sci_not_spars[0]) + 1) + sci_not_spars[3:]  # skip dot
    else:
        assert False, f'precision=1 but neither ceil nor exactly precision=0. sci_not_spars={sci_not_spars}'
    return sci_not_spars

def readable_p(p_val):
    '''Convert a scientific-notation p-value (str) to a readable string (to be formated by matplotlib).
    Always ceil the decimal (for rounding, see readable_p_exact()). 
    If a float is given, it is first converted to a string using two_digit_sci_not().'''

    if type(p_val) != str:
        p_val = two_digit_sci_not(x=p_val)
    if p_val[2] == 'e':
        assert p_val[:4] == '10e-', p_val
        tmp_exp = int(p_val[-2:])
        p_val = f'1e-{str(tmp_exp - 1).zfill(2)}'

    if len(p_val) > 5:
        assert len(p_val) == 6 and p_val[1:3] == 'e-', p_val 
        exponent = p_val[-3:]
        read_p = f'{p_val[0]}x' + r"$10^{{-{tmp}}}$".format(tmp=exponent)  # for curly brackets explanation see https://stackoverflow.com/questions/53781815/superscript-format-in-matplotlib-plot-legend
    else:
        if p_val == '1e+00' or p_val == '1e-00':
            read_p = '1.0'
        else:
            assert p_val[2] == '-', f'p value is greater than 1, p val: {p_val}'

            if p_val[-3:] == '-01':
                read_p = f'0.{p_val[0]}'
            elif p_val[-3:] == '-02':
                read_p = f'0.0{p_val[0]}'
            elif p_val[-3:] == '-03':
                read_p = f'0.00{p_val[0]}'
            else:
                if int(p_val[-2:]) < 10:
                    exponent = p_val[-1]
                else:
                    exponent = p_val[-2:]
                read_p = f'{p_val[0]}x' + r"$10^{{-{tmp}}}$".format(tmp=exponent)  # for curly brackets explanation see https://stackoverflow.com/questions/53781815/superscript-format-in-matplotlib-plot-legend
    return read_p

def readable_p_exact(p_val):
    '''Convert a p-value (float) to a readable string, without ceiling.'''
    if type(p_val) !=  float:
        p_val = float(p_val)

    if p_val >= 0.01:
        read_p = str(np.round(p_val, 2))
    elif p_val >= 0.001: 
        read_p = str(np.round(p_val, 3))
    else:
        tmp = np.format_float_scientific(p_val, precision=0)  # round to nearest
        p_val = tmp[0] + tmp[2:]  # skip dot
        if p_val[2] == 'e':
            assert p_val[:4] == '10e-', p_val
            tmp_exp = int(p_val[-2:])
            p_val = f'1e-{str(tmp_exp - 1).zfill(2)}'

        if len(p_val) > 5:
            assert len(p_val) == 6 and p_val[1:3] == 'e-', p_val 
            exponent = p_val[-3:]
            read_p = f'{p_val[0]}x' + r"$10^{{-{tmp}}}$".format(tmp=exponent)  # for curly brackets explanation see https://stackoverflow.com/questions/53781815/superscript-format-in-matplotlib-plot-legend
        else:
            assert p_val[2] == '-', f'p value is greater than 1, p val: {p_val}'

            if int(p_val[-2:]) < 10:
                exponent = p_val[-1]
            else:
                exponent = p_val[-2:]
            read_p = f'{p_val[0]}x' + r"$10^{{-{tmp}}}$".format(tmp=exponent)  # for curly brackets explanation see https://stackoverflow.com/questions/53781815/superscript-format-in-matplotlib-plot-legend

            if read_p == '1x$10^{-3}$':  # can happen from rounding up fronm eg 0.0099 
                read_p = '0.001'
    return read_p

def readable_p_significance_statement(p_val, n_bonf=None,
                                      upper_criterion_1_asterisk=0.05,
                                      upper_criterion_2_asterisks=0.01,
                                      upper_criterion_3_asterisks=0.001):
    '''Convert a p-value (float) to significance notation (p < 0.001, p < 0.01, p < 0.05, n.s.; as well as asterisks).'''
    assert type(upper_criterion_1_asterisk) == float
    assert type(upper_criterion_2_asterisks) == float
    assert type(upper_criterion_3_asterisks) == float

    if type(p_val) != float:
        p_val = float(p_val)
    if n_bonf is None:
        n_bonf = 1

    if p_val < upper_criterion_3_asterisks / n_bonf:
        str_p = f'p < {upper_criterion_3_asterisks}'
        str_short = '***'
    elif p_val < upper_criterion_2_asterisks / n_bonf:
        str_p = f'p < {upper_criterion_2_asterisks}'
        str_short = '**'
    elif p_val < upper_criterion_1_asterisk / n_bonf:
        str_p = f'p < {upper_criterion_1_asterisk}'
        str_short = '*'
    else:
        str_p = f'p = {np.round(p_val, 2)}'
        str_short = 'n.s.'

    return str_p, str_short