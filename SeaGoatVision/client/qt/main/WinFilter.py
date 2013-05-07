#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# thanks for float_qslider.py : https://gist.github.com/justinfx/3427750

from PySide import QtGui
from PySide import QtCore
from SeaGoatVision.commun.param import Param

class WinFilter(QtGui.QDockWidget):
    selectedFilterChanged = QtCore.Signal(object)

    def __init__(self, controller):
        super(WinFilter, self).__init__()
        self.setWidget(QtGui.QWidget())
        self.lst_param = []
        self.controller = controller
        self.cb_param = None
        self.layout = None

    def setFilter(self, execution_name, filter_name):
        del self.lst_param[:]
        self.widget().destroy()
        self.cb_param = None
        self.layout = None
        self.setWidget(QtGui.QWidget())
        self.filter_name = filter_name
        self.execution_name = execution_name
        self.construct_widget()

    def construct_widget(self):
        # TODO when self.execution_name is None, show configuration filterchain params
        self.setWindowTitle("%s - %s" % (self.filter_name, self.execution_name))
        self.filter_param = self.controller.get_params_filterchain(self.execution_name, filter_name=self.filter_name)

        layout = QtGui.QVBoxLayout()
        self.resetButton = QtGui.QPushButton()
        self.resetButton.clicked.connect(self.reset)
        self.resetButton.setText("Reset")
        layout.addWidget(self.resetButton)

        if not self.filter_param:
            nothing = QtGui.QLabel()
            nothing.setText("Empty params.")
            layout.addWidget(nothing)
            self.widget().setLayout(layout)
            return

        # for param in self.filter_param:
        #    layout.addWidget(self.getWidget(param))

        self.layout = layout
        self.cb_param = QtGui.QComboBox()
        for param in self.filter_param:
            self.cb_param.addItem(param.get_name())
            self.lst_param.append(param)
        if self.filter_param:
            self.cb_param.currentIndexChanged.connect(self.on_cb_param_item_changed)
            layout.addWidget(self.cb_param)
            self.on_cb_param_item_changed(0, first=True)


        self.widget().setLayout(layout)

    def on_cb_param_item_changed(self, index, first=False):
        if self.cb_param:
            param_name = self.cb_param.currentText()
            param_list = [param for param in self.lst_param if param.get_name() == param_name]
            if param_list:
                if not first:
                    b = self.layout.itemAt(self.layout.count() - 1)
                    b.widget().deleteLater()
                param = param_list[0]
                self.layout.addWidget(self.getWidget(param))

    def getWidget(self, param):
        groupBox = QtGui.QGroupBox()

        groupBox.setTitle(param.get_name())

        getWidget = {
            int : self.getIntegerWidget,
            float : self.getFloatWidget,
            str : self.getStrWidget,
            bool : self.getBoolWidget,
            }

        def create_value_change(param):
            def set(value):
                if param.get_type() is bool:
                    value = bool(value)
                self.controller.update_param(self.execution_name, self.filter_name, param.get_name(), value)
            return set

        layout = getWidget[param.get_type()](param, create_value_change(param))
        groupBox.setLayout(layout)

        return groupBox

    def getIntegerWidget(self, param, cb_value_change):
        numberLabel = QtGui.QLabel()
        value = param.get()
        if type(value) is tuple:
            numberLabel.setNum(value[0])
        else:
            numberLabel.setNum(value)

        slider = QtGui.QSlider()
        slider.setBaseSize(100, 100)
        if param.get_min() is not None:
            slider.setMinimum(param.get_min())
        if param.get_max() is not None:
            slider.setMaximum(param.get_max())
        slider.setTickInterval(1)
        if type(value) is tuple:
            slider.setValue(value[0])
        else:
            slider.setValue(value)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        slider.valueChanged.connect(numberLabel.setNum)
        slider.valueChanged.connect(cb_value_change)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(numberLabel)
        return layout

    def getFloatWidget(self, param, cb_value_change):
        numberLabel = QtGui.QLabel()
        value = param.get()
        if type(value) is tuple:
            numberLabel.setNum(value[0])
            fake_value = value[0] * 100
        else:
            numberLabel.setNum(value)
            fake_value = value * 100
        self.setNum = numberLabel.setNum
        self.cb_value_change = cb_value_change

        slider = QtGui.QSlider()
        slider.valueChanged.connect(self._float_value_change)
        self.slider_float = slider
        #slider.setBaseSize(100, 100)
        if param.get_min() is not None:
            slider.setMinimum(param.get_min() * 100)
            self._new_slider_min = param.get_min()
        if param.get_max() is not None:
            slider.setMaximum(param.get_max() * 100)
            self._new_slider_max = param.get_max()
        slider.setTickInterval(1)
        slider.setValue(fake_value)

        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(numberLabel)
        return layout

    def fit(self, v, oldmin, oldmax, newmin=0.0, newmax=1.0):
        """
        Just a standard math fit/remap function

            number v         - initial value from old range
            number oldmin     - old range min value
            number oldmax     - old range max value
            number newmin     - new range min value
            number newmax     - new range max value

        Example:

            fit(50, 0, 100, 0.0, 1.0)
            # 0.5

        """
        scale = (float(v) - oldmin) / (oldmax - oldmin)
        new_range = scale * (newmax - newmin)
        if newmin < newmax:
            return newmin + new_range
        else:
            return newmin - new_range

    def _float_value_change(self, value):
        newVal = self.fit(
            value,
            self.slider_float.minimum(), self.slider_float.maximum(),
            self._new_slider_min, self._new_slider_max
        )
        self.setNum(newVal)
        self.cb_value_change(newVal)

    def getStrWidget(self, param, cb_value_change):
        print "string"

    def getBoolWidget(self, param, cb_value_change):
        boolLabel = QtGui.QLabel()
        boolLabel.setNum(param.get())

        checkbox = QtGui.QCheckBox()
        if param.get():
            checkbox.setCheckState(QtCore.Qt.PartiallyChecked)
        checkbox.stateChanged.connect(cb_value_change)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(checkbox)
        layout.addWidget(boolLabel)
        return layout

    def reset(self):
        for param in self.lst_param:
            param.reset()
        self.setFilter(self.execution_name, self.filter_name)
