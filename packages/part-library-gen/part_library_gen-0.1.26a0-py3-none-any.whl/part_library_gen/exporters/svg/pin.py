import drawsvg as svg

pin_spacing = 50
pin_font_size = 40
pin_desc_spacing = 15

in_arrow = svg.Marker(-1.5, -0.61, 0, 0.6, scale=4, orient='auto')
in_arrow.append(svg.Lines(-1, 0.5, -1, -0.5, 0, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))

in_al_arrow = svg.Marker(-2.1, -0.61, 0, 0.6, scale=4, orient='auto')
in_al_arrow.append(svg.Circle(-0.5, 0, 0.5, stroke_width=0.1, fill='gray', stroke='black'))
in_al_arrow.append(svg.Lines(-2, 0.5, -2, -0.5, -1.1, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))

out_arrow = svg.Marker(-1.5, -0.61, 0, 0.6, scale=4, orient='auto')
out_arrow.append(svg.Lines(-1, 0, 0, -0.5, 0, 0.5, stroke_width=0.1, close=True, fill='gray', stroke='black'))

out_al_arrow = svg.Marker(-2.1, -0.61, 0, 0.6, scale=4, orient='auto')
out_al_arrow.append(svg.Circle(-0.5, 0, 0.5, stroke_width=0.1, fill='gray', stroke='black'))
out_al_arrow.append(
    svg.Lines(-2.1, 0, -1.1, -0.5, -1.1, 0.5, stroke_width=0.1, close=True, fill='gray', stroke='black'))

out_od_arrow = svg.Marker(-1.5, -0.61, 0, 0.6, scale=4, orient='auto')
out_od_arrow.append(svg.Lines(-1, 0, 0, -0.5, 0, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))

out_od_al_arrow = svg.Marker(-2.1, -0.61, 0, 0.6, scale=4, orient='auto')
out_od_al_arrow.append(svg.Circle(-0.5, 0, 0.5, stroke_width=0.1, fill='gray', stroke='black'))
out_od_al_arrow.append(
    svg.Lines(-2.1, 0, -1.1, -0.5, -1.1, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))

bidirectional_arrow = svg.Marker(-2.3, -0.61, 0, 0.6, scale=4, orient='auto')
bidirectional_arrow.append(
    svg.Lines(-1, 0.5, -1, -0.5, 0, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))
bidirectional_arrow.append(
    svg.Lines(-2.3, 0, -1.3, -0.5, -1.3, 0.5, stroke_width=0.1, close=True, fill='gray', stroke='black'))

marker_map = {"In": in_arrow,
              "InAnalog": None,
              "InDigital": in_arrow,
              "InDigital;ActiveLow": in_al_arrow,
              "InDigital;ActiveHigh": in_arrow,
              "InDigitalClock": in_arrow,
              "Out": out_arrow,
              "OutAnalog": None,
              "OutAnalog;ActiveLow": None,
              "OutDigital": out_arrow,
              "OutDigital;ActiveLow": out_al_arrow,
              "OutDigital;OpenDrain": out_od_arrow,
              "OutDigital;OpenDrain;ActiveLow": out_od_al_arrow,
              "InOut": bidirectional_arrow,
              "PwrIn": None,
              "PwrOut": None,
              "PwrGND": None,
              "PwrInOut": None,
              "NC": None,
              "NC-GND": None,
              "NC-Float": None
              }


def generate_symbol_pin(pin):
    group = svg.Group()
    if pin.rotation == 0:
        pin_end = pin.x + pin.length

        group.append(svg.Line(pin.x,
                              pin.y,
                              pin_end,
                              pin.y,
                              stroke_width=5,
                              stroke='black',
                              marker_end=marker_map[pin.function]))
        if pin.name and pin.name_visible:
            group.append(svg.Text(pin.name,
                                  pin_font_size,
                                  pin_end + pin_desc_spacing,
                                  pin.y + pin_font_size / 4,
                                  text_decoration="overline" if "ActiveLow" in pin.function else None))
        if pin.number:
            if isinstance(pin.number, list) and len(pin.number) == 1:
                pin_no_str = str(pin.number[0])
            else:
                pin_no_str = str(pin.number)
            group.append(svg.Text(pin_no_str,
                                  pin_font_size,
                                  pin_end - 40,
                                  pin.y - 5,
                                  text_anchor='end'))
    elif pin.rotation == 90:
        pin_end = pin.y + pin.length

        group.append(svg.Line(pin.x,
                              pin.y,
                              pin.x,
                              pin_end,
                              stroke_width=5,
                              stroke='black',
                              marker_end=marker_map[pin.function]))
        if pin.name and pin.name_visible:
            group.append(svg.Text(pin.name,
                                  pin_font_size,
                                  pin_end + pin_desc_spacing,
                                  pin.y + pin_font_size / 4,
                                  text_decoration="overline" if "ActiveLow" in pin.function else None))
        if pin.number:
            if isinstance(pin.number, list) and len(pin.number) == 1:
                pin_no_str = str(pin.number[0])
            else:
                pin_no_str = str(pin.number)
            group.append(svg.Text(pin_no_str,
                                  pin_font_size,
                                  pin.x - 5,
                                  pin.y + 60,
                                  text_anchor='end'))
    elif pin.rotation == 180:
        pin_end = pin.x - pin.length
        group.append(svg.Line(pin.x,
                              pin.y,
                              pin_end,
                              pin.y,
                              stroke_width=5,
                              stroke='black',
                              marker_end=marker_map[pin.function]))
        if pin.name:
            group.append(svg.Text(pin.name,
                                  pin_font_size,
                                  pin_end - pin_desc_spacing,
                                  pin.y + pin_font_size / 4,
                                  text_decoration="overline" if "ActiveLow" in pin.function else None,
                                  text_anchor='end'))
        if pin.number:
            if isinstance(pin.number, list) and len(pin.number) == 1:
                pin_no_str = str(pin.number[0])
            else:
                pin_no_str = str(pin.number)
            group.append(svg.Text(pin_no_str,
                                  pin_font_size,
                                  pin_end + 40,
                                  pin.y - 5))
    elif pin.rotation == 270:
        pin_end = pin.y - pin.length

        group.append(svg.Line(pin.x,
                              pin_end,
                              pin.x,
                              pin.y,
                              stroke_width=5,
                              stroke='black',
                              marker_end=marker_map[pin.function]))
        if pin.name and pin.name_visible:
            group.append(svg.Text(pin.name,
                                  pin_font_size,
                                  pin_end + pin_desc_spacing,
                                  pin.y + pin_font_size / 4,
                                  text_decoration="overline" if "ActiveLow" in pin.function else None))
        if pin.number:
            if isinstance(pin.number, list) and len(pin.number) == 1:
                pin_no_str = str(pin.number[0])
            else:
                pin_no_str = str(pin.number)
            group.append(svg.Text(pin_no_str,
                                  pin_font_size,
                                  pin.x - 5,
                                  pin.y - 40,
                                  text_anchor='end'))
    return group
