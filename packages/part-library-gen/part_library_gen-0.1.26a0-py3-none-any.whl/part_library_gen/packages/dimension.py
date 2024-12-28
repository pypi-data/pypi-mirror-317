from decimal import Decimal


class Dimension:
    def __init__(self, typ, min_, max_):
        self.typ = typ
        self.min_ = min_
        self.max_ = max_

    def get_available_max(self):
        if self.max_:
            return self.max_
        if self.typ:
            return self.typ
        if self.min_:
            return self.min_

    @staticmethod
    def from_str(str_dimension):
        dim = Dimension(None, None, None)
        if '~' in str_dimension:
            tmp = str_dimension.split('~')
            dim.min_ = Decimal(tmp[0].replace('mm', ''))
            dim.max_ = Decimal(tmp[1].replace('mm', ''))
        elif '±' in str_dimension:
            tmp = str_dimension.split('±')
            dim.typ = Decimal(tmp[0].replace('mm', ''))
            dim.min_ = dim.typ - Decimal(tmp[1].replace('mm', ''))
            dim.max_ = dim.typ + Decimal(tmp[1].replace('mm', ''))
        elif 'max.' in str_dimension:
            dim.max_ = Decimal(str_dimension.replace('max.', '').replace('mm', ''))
        elif 'min.' in str_dimension:
            dim.min_ = Decimal(str_dimension.replace('min.', '').replace('mm', ''))
        else:
            dim.typ = Decimal(str_dimension.replace('mm', ''))
        return dim
