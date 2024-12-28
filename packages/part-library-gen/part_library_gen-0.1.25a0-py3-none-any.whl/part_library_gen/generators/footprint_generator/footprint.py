

class Footprint:
    def __init__(self, name):
        self.name = name
        self.width = 0
        self.height = 0
        self.pads = []
        self.top_overlay = []
        self.bottom_overlay = []
        self.assembly_top = []

    def add_pad(self, pad):
        if isinstance(pad, list):
            self.pads += pad
        else:
            self.pads.append(pad)

    def add_overlay(self, overlay):
        if isinstance(overlay, list):
            self.top_overlay += overlay
        else:
            self.top_overlay.append(overlay)
