# Better base plot styling, in my opinion. Intended for use
#   with the Bokeh plotting library: http://bokeh.pydata.org

# WORK IN PROGRESS -- @kdodia (Jul 9 2014)
# Compatible with Bokeh 0.5

def seabornify(plt):
    
    import bokeh.objects
    import bokeh.glyphs
    import itertools
    
    # -------------------------------
    # DEFAULTS
    colors = itertools.cycle(['#4c72b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#64b5cd'])
    
    # See https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py
    dark_gray = '#262626'
    light_gray = '#CCCCCC'
    seaborn_gray = '#E8E8E8' # A /shade/ darker than seaborn, actually
    white = '#FFFFFF'

    plot_props = {
        'background_fill': seaborn_gray,
        'outline_line_color': None,
        'title_text_font': 'Arial',
        # TODO fix in docs
        'title_text_font_size': '1.5em',
        'title_text_font_style': 'normal',
        'title_text_color': dark_gray}

    axis_props = {
        'axis_line_color': white,
        'major_tick_label_text_color': dark_gray,
        'axis_label_text_color': dark_gray,
        'major_tick_in': 0,
        'major_tick_out': 0,
        'minor_tick_in': 0, # not working 
        'minor_tick_out': 0}

    
    grid_props = {
        'grid_line_color': white}

    line_props = {
        'solid_capstyle': 'round',
        'line_width': 2,
        'line_join': 'round',
        'line_cap': 'round'}

    legend_props = {
        'border_line_alpha': 0,
#        'background_fill_color': white,
#        'background_fill_alpha': 1
    }
        
    #TODO extend text properties to axis labels, major tick labels, text?, legend? (5)
    #TODO allow more default styles than just "darkgrid". (2)   
    
    
    # -------------------------------
    # HERE WE GOOO
    
    # *Plot* me like one of your French girls
    for prop in (y for y in plot_props if y not in plt._changed_vars):
        plt.set(**{prop: plot_props[prop]})

    # TODO: more basic renderer support; drop the 'if' algorithm and instead match
    #   prop dicts to the renderers. Also explore potential plot splatting.
    for x in plt.renderers:
        
        # We determine the parameters of our *Axis*-tence
        if isinstance(x, bokeh.objects.LinearAxis):
            # Intention: apply styling across the object/glyph,
            #   but respect attributes that appear in `_changed_vars`.
            #   A "no-conflict" of sorts.
            # TODO: This is /not/ efficient. Pythonista review required.
            for prop in (y for y in axis_props if y not in x._changed_vars):
                x.set(**{prop: axis_props[prop]})

            continue
        
        #*Grid*-dle me this...
        if isinstance(x, bokeh.objects.Grid):
            for prop in (y for y in grid_props if y not in x._changed_vars):
                x.set(**{prop: grid_props[prop]})
        
            continue
            
        # This is going to be *Legend*--wait for it--ary!!
        if isinstance(x, bokeh.objects.Legend):
            for prop in (y for y in legend_props if y not in x._changed_vars):
                x.set(**{prop: legend_props[prop]})
        
            continue
        
        # *Lines*, lines, lines
        if isinstance(x, bokeh.objects.Glyph) and \
           isinstance(x.glyph, bokeh.glyphs.Line):
            
            # TODO: Investigate why `line_color` is already set
            if x.glyph.line_color == '#1f77b4' or \
              'line_color' not in x.glyph._changed_vars:
                x.glyph.line_color = next(colors)

            for prop in (y for y in line_props if y not in x.glyph._changed_vars):
                x.glyph.set(**{prop: line_props[prop]})
            
            continue
            
    return
