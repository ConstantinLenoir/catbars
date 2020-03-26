from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.patches as mpatches
import matplotlib.text
import matplotlib.ticker

import numpy as np

from functools import partial
import logging
from io import BytesIO
import pprint

from .models import ModelFactory

from .conf import Conf


class Bars:
    """This class represents a complex horizontal bar chart.

    This class extends (by composition) the functionality provided
    by Matplotlib.
    The chart is automatically rendered in Jupyter notebooks and can
    be saved on disk.
    The chart can be tailored to a great extent by passing keyword
    arguments to the constructor. (SEE the class attribute **Bars.conf**
    for listing the other optional **kwargs**).
    If it is not enough, the **conf.py** module in the Catbars package
    gives users full control over "rcParams".

    Parameters
    -----------    

    numbers : iterable container
        The numbers specifying the width of each bar. First numbers are
        converted into bars appearing on the top of the figure.

    left_labels : iterable container or str, optional
        Labels associated with the bars on the left.
        The "rank" option creates one-based indices.
        The "proportion" option creates labels representing the
        relative proportion of each bar in percents.
        "rank" and "proportion" labels depend on the "slice" unless
        "global_view" is True.

    right_labels : iterable container or str, optional
        Labels associated with the bars on the right. It accepts the same
        values as "left_labels".

    colors : iterable container, optional
        The container items can be of any type. Bar colors are
        automatically inferred in function of the available "tints" (SEE
        Bars.conf) and the most common items in the "slice" (unless
        "global_view is True). If there are more distinct items than
        available "tints", "default_color" and "default_label" are used with
        residual items. The automatic color selection can be overriden
        by "color_dic".

    line_dic : dict, optional
        This dictionary has to contain three keys: "number", "color" and 
        "label". It describes an optional vertical line to 
        draw.

    sort : bool, optional
        If True, "numbers" are sorted in descending order. Optional labels
        and the "colors" parameter are sorted in the same way. The default
        value is False.

    slice : tuple : (start,stop), optional
        start and stop are one-based indices. Slicing precedes sorting unless
        "global_view" is True.

    global_view : bool, optional
        If True, the whole dataset is considered instead of the optional
        slice when sorting, coloring, setting x bounds and creating
        "rank" and "proportion" labels. The default value is False.

    auto_scale : bool, optional
        If True, the logarithmic scale is used when it seems better for
        readability. The default value is False.

    color_dic : dict, optional
        A dictionary mapping "colors" items (keys) to Matplotlib colors
        (values)."colors" items which are not specified by the dic. are
        treated as residual items (SEE "colors").

    title : str, optional
        Figure title.

    xlabel : str, optional
        The Matplotlib xlabel.

    ylabel : str, optional
        The Matplotlib ylabel.

    legend_title : str, optional

    legend_visible : bool, optional
        The default value is True.

    figsize : (width, height), optional
        The Matplotlib figsize. The default value is (6,5).

    dpi : number, optional
        The Matplotlib dpi. The default value is 100.

    file_name : str or path-like or file-like object
        The path of the png file to write to. (SEE the method print_pdf()
        for writing pdf files).

    Returns
    --------
    catbars.bars.Bars
        A Bars instance. It encapsulates useful Matplotlib objects.
    
    
    Attributes
    -----------

    conf : dict
        This class attribute contains the advanced optional
        constructor parameters along with their current values.
        In particular, it contains the "fig_size", "dpi",  "tints",
        "default_color" and "default_label" values.
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes.Axes
    canvas : matplotlib.backends.backend_agg.FigureCanvasAgg
    data : catbars.models.AbstractModel
        The Bars class delegates to another class data processing tasks.

    Methods
    -------
    print_png(file_name)
        To write png files.
    print_pdf(file_name)
        To write pdf files.

    

    """

    conf = Conf.conf

    def __init__(self,
                 numbers,
                 left_labels = None,
                 right_labels = None, # 'proportion' 'rank'
                 colors = None,
                 line_dic = None,
                 sort = False,
                 slice = None, # one-based indexing
                 global_view = False,
                 auto_scale = False,
                 color_dic = None,
                 title = None,
                 xlabel = None,
                 ylabel = None,
                 legend_title = None,
                 legend_visible = True,
                 file_name = None,
                 **kwargs):
        """
        The data space can adapt to long labels but only to
        some extent because the long label sizes are fixed.
        This class moves the edges of the axes to make room
        for labels (SEE Matplotlib HOW-TOs).
        """                        
        if 'log_level' in kwargs:
            logging.basicConfig(format='{levelname}:\n{message}',
                                level= getattr(logging, kwargs['log_level']),
                                style = '{')
            
        # Configuration: matplotlibrc is decorated by conf.py.
        self.conf = Conf.change_conf(kwargs)
        
        # Data formatted by the model.
        self.data = None
        
        
        # Core Matplotlib objects.
        self.fig = None
        self.ax = None
        self.canvas = None
        self.vertical_line = None
        self.bars = None # BarContainer.
        self._virtual_bars  = None # For global_view.

        # Helper attributes.
        self._left_label_data = None
        self._right_label_texts = None
        
        # Titles.
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend_title = legend_title
        
        self._global_view = global_view
        self.legend = None
        self._legend_width = 0
        self.legend_visible = legend_visible
        
        # The vertical line.        
        self.line_x = None
        self.line_label = None
        self.line_color = None
        
        
        # Original position of the axes edges in the figure.
        self._x0 = 0
        self._y0 = 0
        self._width = 1
        self._height = 1



        # To deal with not square figures,
        # only x sizes are adapted.
        self._x_coeff = 1

        

        #########################################################

        # Model.
        factory = ModelFactory(
            numbers,
            global_view = global_view,
            left_labels = left_labels,
            right_labels = right_labels,
            colors = colors,
            sort = sort,
            slice = slice,
            default_label = self.conf['default_label'],
            color_dic = color_dic,
            tints = self.conf['tints'],
            default_color = self.conf['default_color'])
        


        self.data = factory.model
                        
        
        self.fig = Figure(figsize = self.conf['figsize'],
                          dpi = self.conf['dpi'])
        
        self.canvas = FigureCanvasAgg(self.fig)
        
        
        self.ax = Axes(self.fig,
                       [self._x0,
                        self._y0,
                        self._width,
                        self._height])
        
        
        self.fig.add_axes(self.ax)
        self.canvas.draw()
       
        w, h = self.fig.get_size_inches()
        self._x_coeff = h / w
        
        # margin.
        margin = self.conf['margin']
        
        self._x0 = self._x_coeff * margin
        self._y0 = margin
        self._width = self._width - 2 * self._x_coeff * margin
        self._height = self._height - 2 * margin
        
        self._set_position()

                
        self.ax.tick_params(axis = 'y',
                            length = 0)
        
        self.ax.grid(b = True,
                     axis = 'x',
                     which = 'both',
                     color = 'black',
                     alpha = 0.3)
        
        
        for name in ['top', 'right']:
            self.ax.spines[name].set_visible(False)
        
        # xscale.
        if auto_scale is True:
            # To improve clarity.
            if self.data.spread > 1 or self.data.maximum > 1e6:
                self.ax.set(xscale = 'log')
        else:
            formatter = matplotlib.ticker.FuncFormatter(self.float_formatter)
            self.ax.get_xaxis().set_major_formatter(formatter)
        
        
        # Title.
        if self.title is not None:
            self._manage_title()

        
        _kwargs = dict()

        # Left labels.
        if self.data.left_labels is not None:
            _kwargs['tick_label'] = self.data.left_labels 
        else:
            _kwargs['tick_label'] = ''

        # colors.
        if self.data.actual_colors is not None:
            _kwargs['color'] = self.data.actual_colors
        else:
            _kwargs['color'] = self.data.default_color

        # bars.
        self.bars = self.ax.barh(list(range(self.data.length)),
                                 self.data.numbers,
                                 height = 1,
                                 edgecolor = 'white',
                                 linewidth = 1, # 0.4
                                 alpha = self.conf['color_alpha'],
                                 **_kwargs)

        # To fix x bounds, virtual bars are used.
        if self._global_view is True:
            self._virtual_bars = self.ax.barh(
                [0, 0],
                [self.data.minimum,
                 self.data.maximum],
                height = 0.5,
                edgecolor = 'white',
                linewidth = 1, # 0.4
                alpha = self.conf['color_alpha'],
                visible = False)

        
        # The vertical line.
        if line_dic is not None:
            self._set_line(line_dic)
        
            if (self.line_x is not None and
                self.data.minimum <= self.line_x <= self.data.maximum):
                #
                self.vertical_line = self.ax.axvline(
                    self.line_x,
                    ymin = 0,
                    ymax = 1,
                    color = self.line_color,
                    linewidth = 2,
                    alpha = self.conf['color_alpha'])
        

        # Left label constraint solving.
        self._make_room_for_left_labels()

        # ylabel.
        if self.ylabel is not None:
            self._manage_ylabel()
        
        
        # Legend.
        if (self.legend_visible is True and
            self.data.colors is not None):
            #
            self._draw_legend()
            self._make_room_for_legend()
        
        
        # Right labels.
        if self.data.right_labels is not None:
            self._draw_right_labels()            
            self._make_room_for_right_labels()
        
        
        min_tick_y = self._clean_x_ticklabels()
        
        # xlabel.
        if self.xlabel is not None:
            self._manage_xlabel(min_tick_y)
        else:
            delta_y0 = abs(self._y0 - min_tick_y)
            self._y0 = self._y0 + delta_y0
            self._height = self._height - delta_y0
            self._set_position()

        
        self.canvas.draw()
        
        # Printing.
        if file_name is not None:
            self.canvas.print_png(file_name)
        

        
        #############################################################
        
    
    def _set_line(self, line_dic):
        try:
            self.line_x = line_dic['number']
            self.line_label = line_dic['label']
            self.line_color = line_dic['color']
        except Exception:
            text = """
"line_dic" has to define three keys: 'number', 'label' and 'color'.
"""
            raise TypeError(text.strip())


    def _manage_title(self):
        
        pad_in_points = self.fig_coord_to_points(self.fig,
                                                 self.conf['title_pad'],
                                                 axis = 'y')
        title_label = self.ax.set_title(
            self.title,
            pad = pad_in_points,
            fontsize = self.conf['title_font_size'],
            fontweight = 'bold')
        
        self.canvas.draw()
        
        h = title_label.get_window_extent(
            renderer = self.canvas.get_renderer()
            ).height
        
        h_in_fig_coord = self.disp_to_fig_coord(self.fig,
                                                h,
                                                axis = 'y')
        total_h = (h_in_fig_coord +
                   self.conf['title_pad'])
        
        self._height = self._height - total_h
        self._set_position()
    
    
    def _make_room_for_left_labels(self):
        
        """
        Constraint solving for left labels.
        "left_label_data" is stored for further processing and
        will be used to align left and right labels.
        """
        
        
        left_label_data = [] # To align left and right labels.
        min_x = None
        self.canvas.draw()
        for left_label in self.ax.get_yticklabels():
            x, y = left_label.get_position()
            va = left_label.get_va()
            bbox = left_label.get_window_extent(
                    renderer = self.canvas.get_renderer()
                 )
            
            inv = self.fig.transFigure.inverted()
            lab_x, _ = inv.transform((bbox.x0, bbox.y0))
            
            if min_x is None or lab_x < min_x:
                min_x = lab_x # In pixels.
            left_label_data.append((y, va))
        
        delta_x0 = abs(self._x0 - min_x)
        self._x0 = self._x0 + delta_x0
        self._width = self._width - delta_x0
        self._set_position()
        
        self._left_label_data = left_label_data
    
    
    
    def _manage_ylabel(self):
        
        """
        """
        pad = self.fig_coord_to_points(self.fig,
                                       self._x_coeff * self.conf['pad'])
        y_label = self.ax.set_ylabel(
            self.ylabel,
            labelpad = pad,
            fontweight = 'bold',
            fontsize = self.conf['axis_title_font_size'])
        
        self.canvas.draw()
        
        bbox = y_label.get_window_extent(
                    renderer = self.canvas.get_renderer()
                 )
        

        w_in_fig_coord = self.disp_to_fig_coord(self.fig,
                                                bbox.width)
        
        delta_x0 = (w_in_fig_coord +
                    self._x_coeff * self.conf['pad'])
        
        self._x0 = self._x0 + delta_x0
        self._width = self._width - delta_x0 
        self._set_position()
    
        

    def _draw_legend(self):
                
        artists = []
        labels = []
        for i, color in enumerate(self.data.legend_colors):
            # Proxy artists.
            patch = mpatches.Patch(facecolor = color,
                                   alpha = self.conf['color_alpha'])
            artists.append(patch)
            labels.append(self.data.legend_labels[i])
        
        if self.vertical_line is not None:
            artists.append(self.vertical_line)
            labels.append(self.line_label)
        
        kwargs = dict()
        if self.legend_title is not None:
            kwargs['title'] = self.legend_title

        lgd = self.fig.legend(artists,
                              labels,
                              loc ='center left',
                              frameon = False,
                              labelspacing = 0.25,
                              borderpad = 0,
                              borderaxespad = 0,
                              prop = {
                              'size' : self.conf['axis_title_font_size']},
                              **kwargs)
        lgd.get_title().set_fontsize(self.conf['axis_title_font_size'])
        lgd.get_title().set_fontweight('bold')
        lgd.get_title().set_multialignment('center')

        
        self.canvas.draw()
        
        # Constraint solving.
        lgd_width = (lgd.get_window_extent(
                          renderer = self.canvas.get_renderer()
                          ).width)
        
        lgd_width_in_fig_coord = self.disp_to_fig_coord(self.fig,
                                                        lgd_width)
        self.legend = lgd
        self._legend_width = lgd_width_in_fig_coord
        
        logging.info('legend width in pixels {}\n'.format(lgd_width))
        
    

    def _make_room_for_legend(self):
        self.legend.set_bbox_to_anchor((1 -
                                        self._legend_width -
                                        self._x_coeff * self.conf['margin'],
                                        0.5))
        self._width = (self._width -
                       self._legend_width -
                       self._x_coeff *self.conf['pad'])
        self._set_position()
    
    
        
    def _draw_right_labels(self):
        
        """
        Right labels.
        """
        right_label_texts = []
        for i, bar in enumerate(self.bars):
            y, va = self._left_label_data[i]
            w = bar.get_width()
            t = None
            if self.data.right_labels is not None:
                a_right_label = self.data.right_labels[i]
                text = ' {}'.format(a_right_label)
                t = self.ax.text(w, y,
                                 text,
                                 verticalalignment = va,
                                 fontweight = 'normal',
                                 zorder = 10)
                right_label_texts.append(t)
                self.canvas.draw()
        self._right_label_texts = right_label_texts
        
                                
    
    def _make_room_for_right_labels(self):
        
        """
        Constraint solving in figure coordinates.
        A bisection technique is used.
        """
        def _objective_function(coeff_array,
                                label_array,
                                x):
            #
            return max(x, max(coeff_array * x + label_array))

        bar_coeff = []
        text_widths = []
        for i, bar in enumerate(self.bars):
            bar_coeff.append(self._get_bar_coeff(bar))
            t = self._right_label_texts[i]
            text_widths.append(self._get_text_width(t))
        
        coeff_array = np.array(bar_coeff)
        label_array = np.array(text_widths)
        
        f = partial(_objective_function,
                    coeff_array,
                    text_widths)
        
        min_w = self.conf['min_ax_width']
        max_it = self.conf['right_label_max_it']
        tolerance = self.conf['right_label_solver_tolerance']
        
        # Two special cases.
        if f(self._width) == self._width:        
            pass
        # To check whether a solution exists.
        elif f(min_w) < self._width:
            w_b = self._width
            w_a = min_w
            i = 0
            # To prevent from infinite loops.
            while abs(w_b - w_a) > tolerance and i < max_it:
                new_w = w_a + (w_b - w_a) / 2
                if f(new_w) < self._width:
                    w_a = new_w
                else:
                    w_b = new_w
                logging.info('w_a {}\nw_b {}\n'.format(w_a, w_b))
                i += 1
            self._width = w_a
        else:
            self._width = min_w

        self._set_position()

        if i == max_it:
            logging.warning("""
right_label_max_it {} has been hit.
""".format(max_it))
    
    
    def _get_bar_coeff(self, bar):
        """
        bar_width_in_ax_coord can't be greater than 0.95 if
        xmargin = 0.05.
        """
        data_x_one = bar.get_bbox().x1 # Assuming that x0 = 0.
        disp_x_one, _ = self.ax.transData.transform((data_x_one, 0))
        inv = self.ax.transAxes.inverted()
        bar_width_in_ax_coord, _ = inv.transform((disp_x_one, _))
        return bar_width_in_ax_coord


    def _get_text_width(self, t):
        
        t_width = t.get_window_extent(
            renderer = self.canvas.get_renderer()
            ).width # In pixels.
        
        return self.disp_to_fig_coord(self.fig, t_width)
    
    
            
    def _clean_x_ticklabels(self):
        """
        To discard overlaps.
        """
        
        self.canvas.draw()
            
        labels = self.get_visible_ticklabels(
                        self.ax,
                        self.ax.xaxis.get_ticklabels(which = 'both')
                        )
        
        label_bboxes = [lab.get_window_extent(
                             renderer = self.canvas.get_renderer()
                             ) 
                        for lab in labels]
        
        
        current_bbox = label_bboxes[-1]
        min_tick_y = current_bbox.y0
        for i in range(len(label_bboxes) - 1,
                       0,
                       -1):
            if label_bboxes[i-1].overlaps(current_bbox):
                labels[i-1].set_visible(False)
            else:
                current_bbox = label_bboxes[i-1]
                if current_bbox.y0 < min_tick_y:
                    min_tick_y = current_bbox.y0
        inv = self.fig.transFigure.inverted()
        _, tick_y = inv.transform((0, min_tick_y))
        return tick_y
    

    
    def _manage_xlabel(self,
                       min_tick_y):
        """
        min_tick_y is negative.
        """
        pad = self.fig_coord_to_points(self.fig,
                                       self.conf['pad'],
                                       axis = 'y')
        
        x_label = self.ax.set_xlabel(
            self.xlabel,
            labelpad = pad,
            fontweight = 'bold',
            fontsize = self.conf['axis_title_font_size'])
        
        self.canvas.draw()
        bbox = x_label.get_window_extent(
                    renderer = self.canvas.get_renderer()
                 )
        h = self.disp_to_fig_coord(self.fig,
                                   bbox.height,
                                   axis = 'y')
        
        delta_y0 = abs(self._y0 - min_tick_y) + h + self.conf['pad']
        
        self._y0 = self._y0 + delta_y0
        self._height = self._height - delta_y0
        self._set_position()
        
        self.canvas.draw()

    
    def _set_position(self):
        self.ax.set_position([self._x0,
                              self._y0,
                              self._width,
                              self._height])
        positions = ['x0', 'y0', 'width', 'height']
        text = 'Position of the Axes instance edges\n'
        for pos in positions:
            text = text + '{} {}\n'.format(pos, getattr(self, '_'+pos))
        logging.info(text)
                
                
        
    def disp_to_fig_coord(self,
                          fig,
                          dist,
                          axis = 'x'):
        """
        Conversion of a distance from display coordinates
        to figure coordinates.
        """
        w, h = fig.get_size_inches()
        if axis == 'x':
            return dist / (fig.dpi * w)
        else:
            return dist / (fig.dpi * h)

    
    def points_to_fig_coord(self,
                            fig,
                            points,
                            axis = 'x'):
        """
        axis = 'x' refers to the X axis ('y' corresponds to the Y axis).
        There are 72 points per inch.
        """
        w, h = fig.get_size_inches()
        if axis == 'x':
            return (points * 1 / 72) / w
        else:
            return (points * 1 / 72) / h


    def fig_coord_to_points(self,
                            fig,
                            fraction,
                            axis = 'x'):
        """
        axis = 'x' refers to the X axis ('y' corresponds to the Y axis).
        Conversion from figure coordinates to points.
        """
        w, h = fig.get_size_inches()
        if axis == 'x':
            return fraction * w * 72
        else:
            return fraction * h * 72

    
        
    def get_visible_ticklabels(self,
                               ax,
                               labels):
        """
        Only a part of the built labels are displayed by
        the Matplotlib machinary.
        """
        visible_labels = []
        
        x_min, x_max = ax.get_xlim()
        
        for label in labels:
            x = label.get_position()[0]
            if x_min <= x <= x_max:
                if label.get_visible() and label.get_text():
                    visible_labels.append(label)
        return visible_labels


    def float_formatter(self, x, pos):
        """
        Custom scientific notation.
        """
        if x > 1e6 or x < 1e-3:
            text = '{:.1e}'.format(x)
            n, e = text.split('e')
            if float(n) == 0:
                return 0
            e = '{'+ e.lstrip('0+') + '}'
            label = r'${} \times 10^{}$'.format(n, e)
            return label
        else:
            return x


    
    def print_pdf(self, file_name):
        
        from matplotlib.backends.backend_pdf import PdfPages

        pp = PdfPages(file_name)
        pp.savefig(figure = self.fig)
        pp.close()

    def print_png(self, file_name):
        self.canvas.print_png(file_name)


    def _repr_png_(self):
        """
        For notebook integration.
        """
        w, h = self.fig.get_size_inches()
        buf  = BytesIO() # In-memory bytes buffer.
        self.canvas.print_png(buf)
        return (buf.getvalue(),
                {'width' : str(w * self.fig.dpi),
                 'height': str(h * self.fig.dpi)})

