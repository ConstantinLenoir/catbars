Catbars
########
*Simple bars, four features*

Introduction
--------------

Catbars is a Python library for making **horizontal** bar charts.

Built on top of Matplotlib (*barh*), Catbars enables programmers to
visualize efficiently **labelled observations which can be
numerically ordered**.

As a bit of *data science logic* is embedded in Catbars, observations
can be ordered on demand and colors are inferred from labels. You
can override this automatic behaviour by specifying a dictionary
mapping categories to colors. A default color will be used
for the residual categories.

All you have to do is to call the **Bars** constructor with the right
keyword arguments (almost everything can be fine-tuned through *kwargs*).

A special attention has been paid to the layout management. Catbars will
do its best to make room for your data (especially for the long labels
on the left **or on the right**) under the constraint of the figure
size (the classic figsize/dpi combination) and the font sizes (data font,
main title font, axis title font).

Catbars will automatically render the figure in Jupyter notebooks
(implicit *_repr_png_()* call). The figure can be saved on disk in
png format (by specifying the keyword argument *file_name* or by calling
*print_png()* on the returned object) or in pdf format (*print_pdf()*).

Catbars doesn't support grouped bar charts and stacked bar charts.


License
--------
MIT






