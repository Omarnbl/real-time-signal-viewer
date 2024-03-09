from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import numpy as np
import pyqtgraph as pg
import pandas as pd
import os
import random
import sys
import  math
from os import path
from reportlab.lib import colors
from reportlab.platypus import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QShortcut

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ui, _ = loadUiType('ui_try1.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        #LISTS AND NEEDED VARIABLES
        self.signal_data_list = [[],[]]
        self.signal_colors = []
        self.signal_plots = []
        self.signal_data_index = [[],[]]
        self.time_axis = [[],[]]
        self.paused = [False, False]
        self.rewind_running = [False,False]
        self.zoom_out_clicks = [0,0]
        self.zoom_in_clicks = [0,0]
        self.check_boxes=[[],[]]
        self.checked_check_boxes=[[],[]]
        self.colors = []
        self.push_pointer_to_color = {}
        self.push_button_pointer_to_signal_title = {}
        self.export_array = [[], []]
        self.signals_names_to_be_exported = [[], []]
        self.snap_shots_index = 0 #eb2a e3mel clear
        self.snap_shots_stats = []

        #IMPORT BUTTON CHANNEL 1
        self.import_btn = self.findChild(QPushButton, 'import_btn')
        self.import_btn.clicked.connect(lambda: self.load_file())
        #IMPORT BUTTON CHANNEL 2
        self.export_btn = self.findChild(QPushButton, 'export_btn')

        # ZOOM IN FOR BOTH BUTTONS
        self.zoom_in_button_1 = self.findChild(QPushButton, 'channel_1_zoom_in')
        self.zoom_in_button_1.clicked.connect(lambda: self.zoom_button_clicked(False, 1,0.8))
        self.zoom_in_button_2 = self.findChild(QPushButton, 'channel_2_zoom_in')
        self.zoom_in_button_2.clicked.connect(lambda: self.zoom_button_clicked(False,2,0.8))

        # ZOOM OUT FOR BOTH BUTTONS
        self.zoom_out_button_1 = self.findChild(QPushButton, 'channel_1_zoom_out')
        self.zoom_out_button_1.clicked.connect(lambda : self.zoom_button_clicked(False,1,1.25))
        self.zoom_out_button_2 = self.findChild(QPushButton, 'channel_2_zoom_out')
        self.zoom_out_button_2.clicked.connect(lambda: self.zoom_button_clicked(False, 2,1.25))

        # RESET ZOOM
        self.channel_1_reset_zoom_button = self.findChild(QPushButton, 'channel_1_reset_zoom')
        self.channel_1_reset_zoom_button.clicked.connect(lambda : self.reset_view(1))
        self.channel_2_reset_zoom_button = self.findChild(QPushButton, 'channel_2_reset_zoom')

        # AUTO PAN
        self.channel_2_reset_zoom_button.clicked.connect(lambda : self.reset_view(2))
        self.channel_1_auto_pan_button = self.findChild(QPushButton, 'channel_1_auto_pan')
        self.channel_1_auto_pan_button.clicked.connect(lambda:self.enable_x_axis_auto_pan(channel=1))
        self.channel_2_auto_pan_button = self.findChild(QPushButton, 'channel_2_auto_pan')
        self.channel_2_auto_pan_button.clicked.connect(lambda :self.enable_x_axis_auto_pan(channel=2))


        # PAUSE BUTTON CHANNEL 1
        self.pause_button_1 = self.findChild(QPushButton, 'channel_1_pause_btn')
        self.pause_button_1.clicked.connect(lambda: self.pause_graph_button_clicked(1))
        # PAUSE  BUTTON CHANNEL 2
        self.pause_button_2 = self.findChild(QPushButton, 'channel_2_pause_btn')
        self.pause_button_2.clicked.connect(lambda: self.pause_graph_button_clicked(2))

        # REWIND BUTTON CHANNEL 1
        self.rewind_btn_1 = self.findChild(QPushButton, 'channel_1_rewind')
        self.rewind_btn_1.clicked.connect(lambda: self.toggle_rewind(1))
        # REWIND BUTTON CHANNEL 2
        self.rewind_btn_2 = self.findChild(QPushButton, 'channel_2_rewind')
        self.rewind_btn_2.clicked.connect(lambda: self.toggle_rewind(2))


        #SNAPSHOTS
        self.snap_shot_1_btn = self.findChild(QPushButton, 'snap_shot_1_btn')
        self.snap_shot_1_btn.clicked.connect(lambda: self.screenshot_graph(1))
        self.snap_shot_2_btn = self.findChild(QPushButton, 'snap_shot_2_btn')
        self.snap_shot_2_btn.clicked.connect(lambda: self.screenshot_graph(2))

        # EXPORT
        self.export_1_btn = self.findChild(QPushButton, 'export_1_btn')
        self.export_1_btn.clicked.connect(lambda: self.export_graph_to_pdf())

        #GRAPGH WIDGETS
        rgb_color='#ebebeb'
        self.graphs = [pg.PlotWidget(), pg.PlotWidget()]
        self.graphs[0].setBackground(rgb_color)
        self.graphs[1].setBackground(rgb_color)
        self.graphs[0].setMouseEnabled(x=False)
        self.graphs[1].setMouseEnabled(x=False)

        #CONNECTING CHANNEL 1 TO THE GRAPGH WIDGET
        channel_1_widget = self.findChild(QWidget, 'channel_1')
        layout1 = QVBoxLayout(channel_1_widget)
        layout1.addWidget(self.graphs[0])
        # CONNECTING CHANNEL 2 TO THE GRAPGH WIDGET
        channel_2_widget = self.findChild(QWidget, 'channel_2')
        layout2 = QVBoxLayout(channel_2_widget)
        layout2.addWidget(self.graphs[1])

        #INITALIZING Q TIMER 1
        self.timer_1 = QTimer(self)
        self.timer_1.timeout.connect(lambda: self.update(1))
        #INITALIZING Q TIMER 2
        self.timer_2 = QTimer(self)
        self.timer_2.timeout.connect(lambda: self.update(2))

        #SPEED SLIDER 1
        self.speed_slider_1 = self.findChild(QSlider, 'channel_1_speed_slider')
        self.speed_slider_1.valueChanged.connect(lambda value, channel=1: self.update_speed(value, channel))
        self.mapped_speed = 1
        #SPEED SLIDER 2
        self.speed_slider_2 = self.findChild(QSlider, 'channel_2_speed_slider')
        self.speed_slider_2.valueChanged.connect(lambda value, channel=2: self.update_speed(value, channel))
        self.mapped_speed = 1

        #Container for scroll area
        self.scroll_are_container = QWidget(self.scrollArea)
        self.scroll_are_container_layout = QVBoxLayout(self.scroll_are_container)
        self.scrollArea.setWidget(self.scroll_are_container)

        self.signal_data = []

        # SCROLL SLIDER 1 & 2
        self.x_start = 0
        self.x_end = 100
        self.channel_1_horizontal_scroll_slider = self.findChild(QSlider, 'channel_1_horizontal_scroll_slider')
        self.channel_1_horizontal_scroll_slider.valueChanged.connect(lambda value: self.scroll_graph_horizontal(value, channel=1))
        self.channel_1_horizontal_scroll_slider.setDisabled(True)
        self.channel_2_horizontal_scroll_slider = self.findChild(QSlider, 'channel_2_horizontal_scroll_slider')
        self.channel_2_horizontal_scroll_slider.valueChanged.connect(lambda value: self.scroll_graph_horizontal(value, channel=2))
        self.channel_2_horizontal_scroll_slider.setDisabled(True)
        # to store max_signal
        self.max_signal_index = [0, 0]

        # LINK CHANNELS
        self.link_channels_checkbox = self.findChild(QCheckBox, 'link_channels')
        self.rewind_both_timer = QTimer(self)

        # Adding the legends to each graph
        self.legends = [self.graphs[0].addLegend(), self.graphs[1].addLegend()]


        # Create shortcuts
        zoom_in_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        zoom_out_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Z"), self)
        reset_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        import_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        toggle_link_channels_shortcut = QShortcut(QKeySequence("Ctrl+l"), self)

        #Setting the shortcuts
        zoom_in_shortcut.activated.connect(lambda: self.zoom_button_clicked(False, 1, 0.8))
        zoom_in_shortcut.activated.connect(lambda: self.zoom_button_clicked(False, 2, 0.8))
        zoom_out_shortcut.activated.connect(lambda: self.zoom_button_clicked(False, 1, 1.25))
        zoom_out_shortcut.activated.connect(lambda: self.zoom_button_clicked(False, 2, 1.25))
        reset_shortcut.activated.connect(lambda: self.reset_view(1))
        reset_shortcut.activated.connect(lambda: self.reset_view(2))
        import_shortcut.activated.connect(self.load_file)
        toggle_link_channels_shortcut.activated.connect(self.toggle_link_channels)

        QApplication.processEvents()

    def toggle_link_channels(self):
        # Toggle the "Link Channels" checkbox's checked state
        self.link_channels_checkbox.setChecked(not self.link_channels_checkbox.isChecked())

    def reset_zoom(self, channel):
        if self.link_channels_checkbox.isChecked():
            self.reset_zoom_both()
        else:
            # Replace these values with the original view range for your specific case
            original_x_min = 0
            original_x_max = 100

            self.graphs[channel - 1].setXRange(original_x_min, original_x_max)
            self.enable_x_axis_auto_pan(channel)

    def reset_zoom_both(self):
        channel = 1
        original_x_min = 0
        original_x_max = 100

        self.graphs[channel - 1].setXRange(original_x_min, original_x_max)
        self.enable_x_axis_auto_pan(channel)

        channel = 2
        original_x_min = 0
        original_x_max = 100

        self.graphs[channel - 1].setXRange(original_x_min, original_x_max)
        self.enable_x_axis_auto_pan(channel)
    def update_x_range(self,channel,x_start,x_end):
            self.graphs[channel-1].setXRange(x_start, x_end)

    def scroll_graph_horizontal(self, value, channel):

        if self.paused[channel - 1]:
            if self.link_channels_checkbox.isChecked():
                self.scroll_graph_horizontal_link_channel(value)
            max_signal_length = max(len(signal_data) for signal_data in self.signal_data_list[channel - 1])
            max_display_range = min(max_signal_length, self.max_signal_index[channel - 1])
            slider_range = self.x_end - self.x_start
            new_x_start = (max_display_range - slider_range) * value / 100
            new_x_end = new_x_start + slider_range

            if new_x_start < 0:
                new_x_start = 0
                new_x_end = slider_range

            if new_x_end > max_display_range:
                new_x_end = max_display_range
                new_x_start = max_display_range - slider_range

            self.x_start = new_x_start
            self.x_end = new_x_end
            self.update_x_range(channel, new_x_start, new_x_end)

    def scroll_graph_horizontal_link_channel(self, value):
        for channel in [1, 2]:  # Iterate through both channels
            if self.paused[channel - 1]:
                max_signal_length = max(len(signal_data) for signal_data in self.signal_data_list[channel - 1])
                max_display_range = min(max_signal_length, self.max_signal_index[channel - 1])
                slider_range = self.x_end - self.x_start
                new_x_start = (max_display_range - slider_range) * value / 100
                new_x_end = new_x_start + slider_range
                if new_x_start < 0:
                    new_x_start = 0
                    new_x_end = slider_range
                if new_x_end > max_display_range:
                    new_x_end = max_display_range
                    new_x_start = max_display_range - slider_range
                self.x_start = new_x_start
                self.x_end = new_x_end
                self.update_x_range(channel, new_x_start, new_x_end)
                self.channel_1_horizontal_scroll_slider.setValue(value)
                self.channel_2_horizontal_scroll_slider.setValue(value)


    def update(self, channel):
        if not self.paused[channel - 1] and not self.rewind_running[channel - 1]:
            for checkbox in range(len(self.check_boxes[channel - 1])):
                if self.check_boxes[channel - 1][checkbox].isChecked():
                    self.checked_check_boxes[channel - 1].append(checkbox)
            self.graphs[channel - 1].clear()
            temp_signals_names_list = [[], []]
            for signal in self.checked_check_boxes[channel - 1]:
                # Getting the color of each signal from the dictionary
                colors_keys_list = list(self.push_pointer_to_color.keys())
                signal_color = self.push_pointer_to_color[colors_keys_list[signal]]
                # Getting the label of each signal from the dictionary
                labels_keys_list = list(self.push_button_pointer_to_signal_title.keys())
                # storing the values of the signals names in a seperate array for exporting
                signal_label = self.push_button_pointer_to_signal_title[labels_keys_list[signal]]
                temp_signals_names_list[channel - 1].append(signal_label)
                if self.signal_data_index[channel - 1][signal] < len(self.signal_data_list[channel - 1][signal]):
                    # Accumulate the data up to the current index
                    accumulated_data = self.signal_data_list[channel - 1][signal][
                                       :self.signal_data_index[channel - 1][signal] + 1]
                    # Display the entire accumulated data
                    self.graphs[channel - 1].plot(self.time_axis[channel - 1][:len(accumulated_data)], accumulated_data,
                                                  pen=pg.mkPen(color=signal_color, width=2), name=signal_label)
                    self.signal_data_index[channel - 1][signal] += 1

                # Update the maximum signal index for the channel
            self.max_signal_index[channel - 1] = max(self.signal_data_index[channel - 1])
            # Storing the index values to be used in exporting
            self.export_array[channel - 1] = self.checked_check_boxes[channel - 1][:]
            # Storing the signal names to be used for exporting
            self.signals_names_to_be_exported[channel - 1] = temp_signals_names_list[channel - 1][:]
            # CLEAR POINTER CHECKED LIST
            temp_signals_names_list[channel - 1].clear()
            self.checked_check_boxes[channel - 1].clear()
            # START AUTO PAN
            for data_point in range(len(self.signal_data_index[channel - 1])):
                if (self.signal_data_index[channel - 1][data_point] == 150):
                    self.enable_x_axis_auto_pan(channel)

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        imported_files_paths, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "All Files (*)", options=options)
        if imported_files_paths:
            try:
                for dat_file in imported_files_paths:
                    with open(dat_file, 'rb') as file:
                        data = file.read()
                        self.signal_data = np.frombuffer(data, dtype=np.int16)
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        # Append the new signal data and color to their respective lists
                        self.signal_data_list[0].append(self.signal_data)
                        self.signal_data_list[1].append(self.signal_data)
                        self.signal_data_index[0].append(0)
                        self.signal_data_index[1].append(0)
                        self.time_axis[0] = np.linspace(0, len(self.signal_data_list[0][0]),
                                                        len(self.signal_data_list[0][0]))
                        self.time_axis[1] = np.linspace(0, len(self.signal_data_list[1][0]),
                                                        len(self.signal_data_list[1][0]))
                        self.signal_colors.append(color)
                        # Changing the color variable into a QColor Variable
                        color = QColor(color[0], color[1], color[2])
                        file_name = os.path.basename(dat_file)
                        # Create a new QGroupBox for the file
                        file_groupbox = QGroupBox()
                        # Add style to the QGroupBox (border and background)
                        file_groupbox.setStyleSheet("QGroupBox {border: 2px solid gray; background-color: #ffffff;}")
                        # Create an input box (QLineEdit) for the file
                        New_label_box = QLineEdit(file_groupbox)
                        # Create a button to update the label
                        update_button = QPushButton("Update Label")

                        # Set the title of the QGroupBox to an empty string initially
                        file_groupbox.setTitle(f"{file_name}")
                        # Create two checkboxes with object names based on the file name and number
                        self.check_boxes[0].append(QCheckBox("Channel 1", file_groupbox))
                        self.check_boxes[0][len(self.check_boxes[0])-1].setChecked(True)
                        self.check_boxes[1].append(QCheckBox(" Channel 2", file_groupbox))
                        # Creating the Select color for each signal
                        color_button = QPushButton("Select Color", file_groupbox)
                        # Adding the pointer of the push button into the dictionary and setting its
                        # value to the color
                        self.push_pointer_to_color[color_button] = color
                        self.push_button_pointer_to_signal_title[update_button] = f"{file_name}"
                        # Calling to connect set color button function
                        self.connect_set_color_buttons(color_button, color)
                        # Calling to connect update label function
                        self.connect_set_label_buttons(update_button, file_groupbox, New_label_box)
                        # Create a vertical layout for the input box, button, and checkboxes
                        vbox_layout = QVBoxLayout(file_groupbox)
                        vbox_layout.addWidget(New_label_box)
                        vbox_layout.addWidget(update_button)
                        vbox_layout.addWidget(color_button)
                        vbox_layout.addWidget(self.check_boxes[0][len(self.check_boxes[0]) - 1])
                        vbox_layout.addWidget(self.check_boxes[1][len(self.check_boxes[1]) - 1])
                        # Set the layout for the file's QGroupBox
                        file_groupbox.setLayout(vbox_layout)
                        # Add the file's QGroupBox to the container
                        self.scroll_are_container_layout.addWidget(file_groupbox)
                        self.scrollArea.setWidgetResizable(True)
                        self.timer_1.start(100)
                        self.timer_2.start(100)
                        #TA3ALA HENA LW 3AWEZ EL DEFAULT SIGNAL EL MARSOOMA



            except Exception as e:
                print(f'Error reading DAT file: {str(e)}')

            except Exception as e:
                print(f'Error reading DAT file: {str(e)}')

    # Funtion used to connect each set button color using a pointer to the button
    def connect_set_color_buttons(self, psh_button, color):
        psh_button.clicked.connect(lambda: self.set_signal_color_in_dictionary(psh_button, color))

    def connect_set_label_buttons(self, psh_button, groupbox, label_input_box):
        psh_button.clicked.connect(lambda: self.set_new_labels(psh_button, groupbox, label_input_box))

    def set_new_labels(self, psh_button, groupbox, label_input_box):
        new_label = label_input_box.text()
        if new_label:
            groupbox.setTitle(new_label)
            self.push_button_pointer_to_signal_title[psh_button] = new_label

    # Function used to create a color dialog to get the color of the signal and adding it to the dictionary

    def set_signal_color_in_dictionary(self, psh_button, color):
        color = QColorDialog.getColor(initial=color)
        if color.isValid():
            self.push_pointer_to_color[psh_button] = color
    def rewind(self,channel):
        for check_box in range(len(self.check_boxes[channel - 1])):
            if self.check_boxes[channel - 1][check_box].isChecked():
                self.checked_check_boxes[channel - 1].append(check_box)
        if not self.paused[channel - 1]:
            self.graphs[channel - 1].clear()
        for signal in self.checked_check_boxes[channel-1]:
            if not self.paused[channel-1]:
                # DECREMENT THE INDEX
                self.signal_data_index[channel-1][signal] -= 3
                # ENSURE INDEX WITHIN BOUNDS
                if self.signal_data_index[channel-1][signal] < 0:
                    self.signal_data_index[channel-1][signal] = 0
                # UPDATE THE PLOT
                if self.signal_data_index[channel-1][signal] < len(self.signal_data_list[channel-1][signal]):
                    portion = self.signal_data_list[channel-1][signal][:self.signal_data_index[channel-1][signal] + 1]
                    self.graphs[channel-1].plot(self.time_axis[channel-1][:len(portion)], portion, pen=pg.mkPen(color=self.signal_colors[signal], width=2))
        # CLEAR POINTER CHECKED LIST
        self.checked_check_boxes[channel - 1].clear()
    def toggle_rewind(self,channel):
        # TOGGLE THE REWIND FLAG
        if self.link_channels_checkbox.isChecked():
            self.rewind_both()
        else:
            self.rewind_running[channel-1] = not self.rewind_running[channel-1]
            if self.rewind_running[channel-1]:
                self.start_rewind(channel)
            else:
                self.rewind_timer.stop()

    def rewind_both(self):
        self.rewind_running[0] = not self.rewind_running[0]
        self.rewind_running[1] = not self.rewind_running[1]
        if self.rewind_running[0] or self.rewind_running[1]:
            self.start_rewind_both()
        else:
            self.stop_rewind_both()

    def start_rewind(self,channel):
        # START QTIMER
        self.rewind_timer = QTimer(self)
        self.rewind_timer.timeout.connect(lambda: self.rewind(channel))
        self.rewind_timer.start(100)
    def start_rewind_both(self):
        # START QTIMER
        self.rewind_both_timer.timeout.connect(lambda: self.rewind(1))
        self.rewind_both_timer.timeout.connect(lambda: self.rewind(2))
        self.rewind_both_timer.start(100)

    def stop_rewind(self):
        #STOP QTIMER
        if self.rewind_timer.isActive():
            self.rewind_timer.stop()
    def stop_rewind_both(self):
        # STOP QTIMER
        if self.rewind_both_timer.isActive():
            self.rewind_both_timer.stop()



    def pause_graph_button_clicked(self,channel):
        if(self.link_channels_checkbox.isChecked()):
            self.pause_both(channel)
        else:
            #TOGGLE THE PAUSE BUTTON
            if not self.paused[channel-1]:
                self.paused[channel-1] = True
                if channel==1:
                    self.timer_1.stop()
                    self.pause_button_1.setText("Resume")
                    self.speed_slider_1.setEnabled(False)
                    self.channel_1_horizontal_scroll_slider.setEnabled(True)
                else:
                    self.timer_2.stop()
                    self.pause_button_2.setText("Resume")
                    self.speed_slider_2.setEnabled(False)
                    self.channel_2_horizontal_scroll_slider.setEnabled(True)
            else:
                self.paused[channel-1] = False
                if channel==1:
                    self.timer_1.start()
                    self.pause_button_1.setText("Pause")
                    self.speed_slider_1.setEnabled(True)
                    self.channel_1_horizontal_scroll_slider.setEnabled(False)
                    self.channel_1_horizontal_scroll_slider.setValue(0)
                else:
                    self.timer_2.start()
                    self.pause_button_2.setText("Pause")
                    self.speed_slider_2.setEnabled(True)
                    self.channel_2_horizontal_scroll_slider.setEnabled(False)
                    self.channel_2_horizontal_scroll_slider.setValue(0)


    def pause_both(self,channel):
        if not self.paused[1] or not self.paused[0]:
            self.paused[0] = True
            self.paused[1] = True
            self.timer_1.stop()
            self.pause_button_1.setText("Resume")
            self.speed_slider_1.setEnabled(False)
            self.channel_1_horizontal_scroll_slider.setEnabled(True)

            self.timer_2.stop()
            self.pause_button_2.setText("Resume")
            self.speed_slider_2.setEnabled(False)
            self.channel_2_horizontal_scroll_slider.setEnabled(True)
        else:
            self.paused[0] = False
            self.paused[1] = False
            self.timer_1.start()
            self.pause_button_1.setText("Pause")
            self.speed_slider_1.setEnabled(True)
            self.channel_1_horizontal_scroll_slider.setEnabled(False)

            self.timer_2.start()
            self.pause_button_2.setText("Pause")
            self.speed_slider_2.setEnabled(True)
            self.channel_2_horizontal_scroll_slider.setEnabled(False)


    # Function to control speed
    def update_speed(self, value, channel):
        if self.link_channels_checkbox.isChecked():
            self.update_speed_for_both(value)
        else:
            self.speed_slider_1.setEnabled(True)
            min_speed = 1
            max_speed = 10
            self.mapped_speed = min_speed + (max_speed - min_speed) * value / 100
            self.time_step = 1 / (1000 * self.mapped_speed)
            timer_interval = int(100 / self.mapped_speed)
            if channel==1:
                self.timer_1.setInterval(timer_interval)  # Set the new timer interval
            else:
                self.timer_2.setInterval(timer_interval)

    def update_speed_for_both(self, value):
        self.speed_slider_1.setEnabled(True)
        min_speed = 1
        max_speed = 10
        self.mapped_speed = min_speed + (max_speed - min_speed) * value / 100
        self.time_step = 1 / (1000 * self.mapped_speed)
        timer_interval = int(100 / self.mapped_speed)
        self.timer_1.setInterval(timer_interval)  # Set the new timer interval
        self.timer_2.setInterval(timer_interval)
        self.speed_slider_1.setValue(value)
        self.speed_slider_2.setValue(value)

    def screenshot_graph(self, channel):
        pixmap = self.graphs[channel - 1].grab()
        image_path = f'channel_{self.snap_shots_index}_graph.png'
        pixmap.save(image_path)
        self.snap_shots_stats.append(self.generate_statistics_table(channel))
        self.snap_shots_index += 1


    def export_graph_to_pdf(self):
        # Take a screenshot of the graph and save it as an image

        # Show a file dialog to choose the save location
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, f'Save PDF', "", "PDF Files (*.pdf)",
                                                   options=options)

        if file_path:
            # Create a PDF document
            c = canvas.Canvas(file_path, pagesize=letter)
            # Add a title at the top of the page centered horizontally with a blue font color
            title = f'Report'
            c.setFont("Helvetica", 18)
            title_width = c.stringWidth(title, "Helvetica", 18)
            page_width, page_height = letter
            x = (page_width - title_width) / 2
            c.setFillColor(colors.blue)  # Set the font color to blue
            c.drawString(x, page_height - 50, title)
            # Insert the image into the PDF
            for i in range(self.snap_shots_index):
                img_path = f'channel_{i}_graph.png'
                c.drawImage(img_path, 100, 400, width=400, height=200)
                # Generate and insert the statistics table
                stats_df = self.snap_shots_stats[i]
                if stats_df is not None:
                    stats_data = [stats_df.columns.tolist()] + stats_df.values.tolist()
                    stats_table = Table(stats_data)
                    # Define the style for the table
                    style = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ])
                    stats_table.setStyle(style)
                    # Draw the table on the PDF
                    stats_table.wrapOn(c, 400, 600)
                    stats_table.drawOn(c, 100, 250)
                    c.showPage()



            # Save and close the PDF
            c.save()
            #RESET
            self.snap_shots_index =0
            self.snap_shots_stats.clear()

    def generate_statistics_table(self, channel):
        data = []
        for i in self.export_array[channel - 1]:
            data.append(self.signal_data_list[channel - 1][i])
        print(data)
        if not data:
            print("No data available.")
            return

        # Create a list of DataFrames for each list in data
        signal_names = [[], []]
        signal_names[channel - 1] = self.signals_names_to_be_exported[channel - 1][:]
        dfs = []
        for i, sublist in enumerate(data):
            signal_name = signal_names[channel - 1][i] if i < len(signal_names[channel - 1]) else f"Signal {i}"
            mean = pd.Series(sublist).mean()
            std_dev = np.round(pd.Series(sublist).std(), decimals=2)
            duration = len(sublist)  # Assuming each data point represents 1 second
            min_value = min(sublist)
            max_value = max(sublist)
            df = pd.DataFrame({
                "Signal Name": [signal_name],
                "Mean": [mean],
                "Standard Deviation": [std_dev],
                "Duration (s)": [duration],
                "Min Value": [min_value],
                "Max Value": [max_value]
            })
            dfs.append(df)
        # Concatenate the DataFrames into one
        stats_df = pd.concat(dfs)

        return stats_df

    def zoom_button_clicked(self, reset=False, channel=1, factor=0.8):
        if self.link_channels_checkbox.isChecked():
            self.zoom_button_clicked_for_both(False, channel, factor)
        else:
            if not reset:
                if factor == 0.8:
                    self.zoom_in_clicks[channel - 1] += 1
                else:
                    self.zoom_out_clicks[channel - 1] += 1

            # Get the current visible X-axis range
            current_x_min, current_x_max = self.graphs[channel - 1].viewRange()[0]
            # Calculate the new X-axis range (e.g., zoom in by half)
            new_x_min = current_x_min + (current_x_max - current_x_min) * factor
            new_x_max = current_x_max - (current_x_max - current_x_min) * factor

            # Update the X-axis range
            self.graphs[channel - 1].setXRange(new_x_min, new_x_max)
            self.enable_x_axis_auto_pan(channel)

    def zoom_button_clicked_for_both(self, reset=False, channel=1, factor=0.8):
        channel = 1
        if not reset:
            if factor == 0.8:
                self.zoom_in_clicks[channel - 1] += 1
            else:
                self.zoom_out_clicks[channel - 1] += 1

        # Get the current visible X-axis range
        current_x_min, current_x_max = self.graphs[channel - 1].viewRange()[0]
        # Calculate the new X-axis range (e.g., zoom in by half)
        new_x_min = current_x_min + (current_x_max - current_x_min) * factor
        new_x_max = current_x_max - (current_x_max - current_x_min) * factor

        # Update the X-axis range
        self.graphs[channel - 1].setXRange(new_x_min, new_x_max)
        self.enable_x_axis_auto_pan(channel)
        channel = 2
        if not reset:
            if factor == 0.8:
                self.zoom_in_clicks[channel - 1] += 1
            else:
                self.zoom_out_clicks[channel - 1] += 1

        # Get the current visible X-axis range
        current_x_min, current_x_max = self.graphs[channel - 1].viewRange()[0]
        # Calculate the new X-axis range (e.g., zoom in by half)
        new_x_min = current_x_min + (current_x_max - current_x_min) * factor
        new_x_max = current_x_max - (current_x_max - current_x_min) * factor

        # Update the X-axis range
        self.graphs[channel - 1].setXRange(new_x_min, new_x_max)
        self.enable_x_axis_auto_pan(channel)

    def enable_x_axis_auto_pan(self, channel):
        if self.link_channels_checkbox.isChecked():
            self.graphs[1].getPlotItem().getViewBox().enableAutoRange(pg.ViewBox.XAxis)
            self.graphs[1].getPlotItem().getViewBox().setAutoPan(x=True)
            self.graphs[0].getPlotItem().getViewBox().enableAutoRange(pg.ViewBox.XAxis)
            self.graphs[0].getPlotItem().getViewBox().setAutoPan(x=True)
        else:
            self.graphs[channel - 1].getPlotItem().getViewBox().enableAutoRange(pg.ViewBox.XAxis)
            self.graphs[channel - 1].getPlotItem().getViewBox().setAutoPan(x=True)

    def random_color(self):
        # Generate a random color for the new signal
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return color
def main():
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()