import unittest
from os.path import abspath, exists
import hashlib

import pandas as pd
import catbars



class TestLayoutStability(unittest.TestCase):
    """
    This test has to be run with the working directory set
    to 'tests/'.
    """
    def setUp(self):        
        df = pd.DataFrame(
            {'numbers' : [1, 10, 2, 8],
             'name' : ['one', 'ten', 'two', 'height'],
             'parity' : ['odd', 'even', 'even', 'even'],
             'french_name' : ['un', 'dix', 'deux', 'huit']})
        conf ={
            
            'right_label_max_it' : 1000,

            'min_ax_width' : 0.01,
            
            'right_label_solver_tolerance' : 0.001,
            
            'figsize' : (8, 4),
            
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
            
            'margin' : 0.01,
            
            'title_pad' : 0.2,
            
            'pad' : 0.2,
        
            'title_font_size' : 16,
        
            'axis_title_font_size' : 10,
        
            'data_font_size' : 8,

            'max_it' : 1000
            }
        xlabel = """
Feature 1
This feature is a very interesting feature
that requires many explanations""".strip()
        ylabel = """
Feature 2 and 3
Bars can be tagged with two labels""".strip()
        title = """
With $\mathtt{Catbars}$,
you concatenate bars""".strip()
        legend_title = """
Feature 4
The legend text can be very long""".strip()
        self.bars = catbars.Bars(df['numbers'],
                                 right_labels = df['name'],
                                 labels = df['french_name'],
                                 colors = df['parity'],
                                 line_dic = {
                                     'number' : 7,
                                     'color' : 'red',
                                     'label' : 'Seven'},
                                 sort = True,
                                 xlabel = xlabel,
                                 ylabel = ylabel,
                                 title = title,
                                 legend_title = legend_title,
                                 legend_visible = True,
                                 **conf,
                                 log_level = 'INFO')


    def test_stability(self):
        self.assertIsNotNone(self.bars)
        self.bars.print_png(abspath('outputs/new_figure.png'))
        b, _ = self.bars._repr_png_()
        new_code = hashlib.sha1(b).hexdigest()
        path_name = 'hashcodes/stable_figure_hash.txt'
        if exists(abspath(path_name)):
            with open(abspath(path_name)) as f:
                old_code = f.readline()
            
            self.assertEqual(old_code, new_code,
                             'The figure has changed')
        else:
            with open(abspath(path_name), mode = 'w') as f:
                old_code = f.write(new_code)
            text = """
There is no existing hash for the figure.
A new hash has been created""".strip()
            self.skipTest(text)
        
        

if __name__ == '__main__':
    unittest.main()
