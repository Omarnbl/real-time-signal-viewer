# Multi-Port, Multi-Channel Signal Viewer

## Overview

Monitoring vital signals in an ICU setting is essential for patient care. This desktop application, developed using Python and Qt, provides a multi-port, multi-channel signal viewer with the following features:

- **Signal File Import**: Users can browse their PC to open signal files, including samples of different medical signals such as ECG, EMG, EEG, etc., with examples of both normal and abnormal signals.
- **Dual Graphs**: The application contains two identical graphs, each with its own controls. Users can open different signals in each graph and run them independently or link both graphs together. When linked, the graphs display the same time frames, signal speed, and viewport settings.
- **Cine Mode**: Signals are displayed in cine mode, simulating real-time monitoring as seen in ICU monitors. Signals can be paused, played, rewound, and manipulated in real-time through various UI elements.
- **Signal Manipulation**: Users can manipulate running signals by changing color, adding labels/titles, showing/hiding signals, customizing cine speed, zooming, panning, and moving signals between graphs. Boundary conditions are enforced to prevent unintended manipulation beyond signal limits.
- **Exporting & Reporting**: Users can generate a report in PDF format containing snapshots of the graphs and data statistics for the displayed signals, including mean, standard deviation, duration, minimum, and maximum values.

## Libraries Used

- **PyQt5**: For building the desktop application GUI.
- **pyqtgraph**: For real-time plotting and visualization of signals.
- **pandas**: For data manipulation and statistics generation.
- **matplotlib**: For additional plotting capabilities.
- **numpy**: For numerical operations and signal processing.

## Preview

![Preview Gif](/Task_1/Design/Animation.gif)

![Main View](/Task_1/Design/Main.png)

![Export Options](/Task_1/Design/Export.png)

![Color Setting](/Task_1/Design/set_color.png)


## Contributors <a name = "Contributors"></a>


## Contributors <a name = "Contributors"></a>
<table>
  <tr>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/OmarEmad101">
          <img src="https://github.com/OmarEmad101.png" width="100px" alt="@OmarEmad101">
          <br>
          <sub><b>Omar Emad</b></sub>
        </a>
      </div>
    </td>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/Omarnbl">
          <img src="https://github.com/Omarnbl.png" width="100px" alt="@Omarnbl">
          <br>
          <sub><b>Omar Nabil</b></sub>
        </a>
      </div>
    </td>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/KhaledBadr07">
          <img src="https://github.com/KhaledBadr07.png" width="100px" alt="@KhaledBadr07">
          <br>
          <sub><b>Khaled Badr</b></sub>
        </a>
      </div>
    </td>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/merna-abdelmoez">
          <img src="https://github.com/merna-abdelmoez.png" width="100px" alt="@merna-abdelmoez">
          <br>
          <sub><b>Mirna Abdelmoez</b></sub>
        </a>
      </div>
    </td>
  </tr>
</table>


## Acknowledgments

**This project was supervised by Dr. Tamer Basha & Eng. Abdallah Darwish, who provided invaluable guidance and expertise throughout its development as a part of the Digital Signal Processing course at Cairo University Faculty of Engineering.**

<div style="text-align: right">
    <img src="https://imgur.com/Wk4nR0m.png" alt="Cairo University Logo" width="100" style="border-radius: 50%;"/>
</div>
