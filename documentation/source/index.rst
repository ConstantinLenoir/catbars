.. elasticbars documentation master file, created by
   sphinx-quickstart on Wed Mar 18 12:22:38 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Catbars: simple bars, four features
========================================

Catbars concatenates bars in various ways at the expense of a simple
class constructor call. Catbars is built on top of Matplotlib
and extends the functionality of *barh*. Boilerplate code is
encapsulated and new features are provided.

Created bar charts are well integrated with Jupyter notebooks and can be
saved on disk with the methods *print_png()* and *print_pdf()*.

.. toctree::
   :maxdepth: 3

   Bars <rst/bars>
   Models <rst/models>
   Conf <rst/conf>
   Documentation <self>   
   

Documentation
===============



.. contents:: Table of contents
   :depth: 2
   :local:

Layout
------

Catbars has its own way to manage the figure layout and then,
doesn't use the Matplotlib tight_layout machinary.

It aims at preventing from overlaps and trims under the constraint
of the figure size in pixels.

To achieve this goal, the figure space is divided into 10 areas which
can be visualized in the following picture. The tenth area is the
data space, also known as the **ax space** (shaded area).

To be more specific, Catbars functions adapt the left bottom point
coordinates as well as the width and the height of the **ax space**
in order to make for the different components (right labels, legend, etc.).



.. image:: /images/anatomy.png


The most sophisticated constraint solving technique used by Catbars consists
in adapating the figure to combinations of resizable bars and fixed labels.
Catbars includes the Matplotlib *xmargin* in its calculations.


Logic
-------

.. code-block:: python

   import pandas as pd
   from catbars import Bars
   import catbars.cac40

   df = pd.DataFrame.from_dict(catbars.cac40.data, 
                            orient = 'index', 
                            columns = ['closing_price', 'cap', 'sector'])
   Bars(df['cap'],
        right_labels = df.index,
    	colors = df['sector'],
    	left_labels = 'rank',
    	sort = True,
    	line_dic = {'number' : df['cap'].median(),
                    'color' : 'black',
                    'label' : 'Median'},
    	title = 'Companies sorted\nby capitalization',
	legend_title = 'Sectors',
        xlabel = 'Capitalization in euros\n{}'.format(catbars.cac40.date),
	ylabel = 'Company names',
	figsize = (7,10))


Catbars embeds data processing features that allow data scientists to 
save time.

Slicing, sorting, color inferring, automatic labelling and
automatic scaling are performed internally on demand through key word
arguments.

Those tasks are delegated to model classes.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
