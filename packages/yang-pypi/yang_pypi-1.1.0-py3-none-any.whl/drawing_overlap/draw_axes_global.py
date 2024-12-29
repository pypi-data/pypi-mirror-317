from matplotlib import pyplot as plt


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance


class DrawAxes:
    _instance = None

    def __init__(self, label_x: str, label_y: str):
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        self.current_label_x = label_x
        self.current_label_y = label_y

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
             cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def drawing(self, x_data, y_data, label_x='', label_y=''):
        self.axes.plot(x_data, y_data)
        if label_x != '' or label_y != '':
            self.current_label_x = label_x
            self.current_label_y = label_y
        self.axes.set_xlabel(self.current_label_x)
        self.axes.set_ylabel(self.current_label_y)

    def canvas_show(self):
        self.figure.show()
        pass


drawing_obj = DrawAxes('x', 'y')
