
from matplotlib import rcdefaults, rcParams
import copy


class Conf:
    """
    Default configuration parameters.

    'max_it' is the maximum number of iterations allowed in
    Bars._adapt_to_right_labels()

    """
    conf ={
        
        'right_label_max_it' : 1000,

        'min_ax_width' : 0.01,
        
        'right_label_solver_tolerance' : 0.001,

        'figsize' : (6, 5),
        
        'dpi' : 100,
        
        'default_color' : 'black',

        'default_label' : 'else',
        
        'tints' : ['#34a854',
                   '#f8b44e',
                   '#d50209',
                   '#5284e5',
                   '#f76c00',
                   '#a8a8a8',
                   '#eb66b4',
                   '#191970',
                   '#6636a9'],
        
        
        'color_alpha' : 0.8,
        
        'margin' : 0.05,
        
        'title_pad' : 0.04,
        
        'pad' : 0.02,
        
        'title_font_size' : 16,
        
        'axis_title_font_size' : 10,
        
        'data_font_size' : 8
        }
        
    def run_conf(conf_dic):
        """
        Settings that are not handled explicitly in bars.py are
        delegated to Matplotlib.
        """
        # To override settings that are not related to Catbars.
        rcdefaults() 
        
        if 'data_font_size' in conf_dic:
            rcParams['font.size'] = conf_dic['data_font_size']
        else:
            rcParams['font.size'] = Conf.conf['data_font_size']


    def change_conf(conf_dic):
        new_conf = copy.deepcopy(Conf.conf)
        for k in conf_dic:
            if k in Conf.conf:
                new_conf[k] = conf_dic[k]

        Conf.run_conf(new_conf)
        return new_conf



