Swatch
======

``swatch`` is a parser for Adobe Swatch Exchange (ASE) files.

Copyright © 2014 Marcos A. Ojeda – http://generic.cx/


With help from documentation on ASE written by
`Carl Camera <http://iamacamera.org/default.aspx?id=109>`_,
and the ASE generator written for 
`colourlovers <https://www.colourlovers.com/>`_ by
`Chris Williams <http://www.colourlovers.com/ase.phps>`_.

``swatch.write(lst, filename)`` reads in a ``list``, as described below,
and outputs a ``.ase`` file.

``swatch.parse(filename)`` reads in an ``.ase`` file and converts it to a
``list`` of colors and palettes. Colors are ``dicts`` in the form::

    {
        'name': 'color name',
        'type': 'Process',
        'data': {
            'mode': 'RGB',
            'values': [1.0, 1.0, 1.0]
        }
    }

The values provided, and their ranges, vary between color mode. For all
color modes, the value is always a ``list`` of floats. The valid ASE modes are:

* **RGB**: three floats between [0, 1]  corresponding to RGB.
* **CMYK**: four floats between [0, 1] inclusive, corresponding to CMYK.
* **Gray**: one float between [0, 1] with 1 being white, 0 being black.
* **LAB**: three floats. The first, L, is ranged from [0, 1]. Both A and B are
  floats ranging from [-128.0, 127.0] – I believe illustrator just crops
  these to whole values, though.

Palettes (or “Color Groups,” in Adobe parlance) are also ``dicts``, but they have an
item named ``swatches`` which contains a ``list`` of colors (as above) in
the palette.::

    {
        'name': 'accent colors',
        'type': 'Color Group',
        'swatches': [
            {color}, {color}, ..., {color}
        ]
    }

Because Adobe Illustrator lets swatches exist either inside and outside
of palettes, the output of ``swatch.parse(…)`` is a ``list`` that may contain
swatches and/or palettes – i.e. ``[ swatch* palette* ]``.

Here’s an example ``dict``, with a single light grey swatch, followed by a
color group containing three more swatches::

    >>> import swatch
    >>> swatch.parse("example.ase")
    [{'data': {'mode': 'Gray', 'values': [0.75]},
      'name': 'Light Grey',
      'type': 'Process'},
     {'name': 'Accent Colors',
      'swatches': [{'data': {'mode': 'CMYK',
         'values': [0.5279774069786072,
          0.24386966228485107,
          1.0,
          0.04303044080734253]},
        'name': 'Green',
        'type': 'Process'},
       {'data': {'mode': 'CMYK',
         'values': [0.6261844635009766,
          0.5890134572982788,
          3.051804378628731e-05,
          3.051804378628731e-05]},
        'name': 'Violet Process Global',
        'type': 'Global'},
       {'data': {'mode': 'LAB', 'values': [0.6000000238418579, -35.0, -5.0]},
        'name': 'Cyan Spot (global)',
        'type': 'Spot'}],
      'type': 'Color Group'}]

Spot, Global and Process Colors
-------------------------------

Something that’s not mentioned in either Carl Camera’s or Chris William’s code
is the mention of spot, global and process colors.

There are three kinds of swatch types available to you in a ASE files: Process,
Global and Spot. Process colors are standard colors, this is the default if you
define a new color in Illustrator. As the name implies, they’re mixed from either
RGB or CMYK depending on the document color mode.

Global colors are the same thing as process colors, but they have one neat property
which is that when you update them, they are updated all throughout your artwork.
This makes them something like “color references,” which are quite useful if you’re
doing something like re-skinning some extant document.

Spot colors are implicitly global, but have the nifty property that you can create
new swatches from them based on “tints” – effectively, some screened value of that
color. The only hitch is that tints, even though they can be part of your file,
can’t be stored or exchanged as swatches. I’m on the fence as to how problematic
this is, but that’s just how it goes. Even Illustrator won’t save them out, it’s
just not supported in the app (almost certainly due to the nature of this file
format).

Caveats
-------

Finally, consider the fact that your swatches can be CMYK a mixed blessing.
While this is invariably useful if you need to import some old swatches for
print work, it will pose a challenge for accurately converting back to RGB or LAB
unless you have a copy of Illustrator handy.

If you don’t, you can always install the color profile calculator from the
(oddly named) `Little CMS <http://www.littlecms.com/>`_ package, feed it the
freely-available SWOP ICC color profile, and use the default output of sRGB
to get your colors into a somewhat usable form for the Web.

If you end up with LAB spot colors, you can always pay
`Bruce Lindbloom’s math page <http://www.brucelindbloom.com/index.html?Math.html>`_
a visit, and have a look at the relatively simple (if somewhat time-consuming)
``LAB->XYZ->RGB`` formulae he has on offer.
