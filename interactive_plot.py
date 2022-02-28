"""
Known errors :
Matplotlib : RuntimeWarning: overflow encountered in multiply
"""

import matplotlib.pyplot as plt
from numpy import isinf, isnan
from matplotlib.widgets import Slider, CheckButtons
from matplotlib.backend_bases import MouseButton
from simple_pid import PID

def get_out_limit(out, step=10):
    out_min, out_max = min(out), max(out)
    ll_out, ul_out = out_min, out_max+step
    ll_out = out_min - step if out_min >= 0 else out_min + (-step)
    if isinf(ll_out) or isnan(ll_out):
        ll_out = 0
    if isinf(ul_out) or isnan(ul_out):
        ul_out = 100
    return ll_out, ul_out

def update_pid_graph():
    global pid, reference_point, reference_plot, pid_plot, axes
    pid.follow(reference_point, 200)
    ref, out, err, timestep = pid.put_data()    
    ll_out, ul_out = get_out_limit(out)
    pid_plot.set_label(
        "{}{}{}".format("P" * pid.k["p"]["state"], "I" * pid.k["i"]["state"], "D" * pid.k["d"]["state"])
    )
    reference_plot.set_data(timestep, ref)
    pid_plot.set_data(timestep, out)
    axes.set_xlim(min(timestep), max(timestep)+.8)
    axes.set_ylim(ll_out, ul_out)
    axes.legend()
    axes.figure.canvas.draw()

def p_slider(slide):
    global pid, reference_point
    pid.k["p"]["value"] = round(slide,2)
    update_pid_graph()

def i_slider(slide):
    global pid, reference_point
    pid.k["i"]["value"] = round(slide,2)
    update_pid_graph()

def d_slider(slide):
    global pid, reference_point
    pid.k["d"]["value"] = round(slide,2)
    update_pid_graph()

def check_box_state(state):    
    global pid, reference_point
    pid.k[state.lower()]["state"] = not pid.k[state.lower()]["state"]
    update_pid_graph()
    
def get_reference_point(event):
    global reference_plot, reference_point
    if event.inaxes is None or event.inaxes.get_lines() is None or (event.inaxes.get_lines()[-1]).get_label() != reference_plot.get_label():
        return
    if event.button is MouseButton.LEFT:
        return
    reference_point = event.ydata
    update_pid_graph()    

def hide_text_box(event):
    global help_text_box, figure
    if event.button != MouseButton.LEFT:
        return
    help_text_box.set_visible(False)
    figure.canvas.draw()

def clean_state():
    global reference_plot, pid_plot, help_text_box, pid, p_slider_widget, i_slider_widget, d_slider_widget
    pid = PID()
    reference_plot.set_data([],[])
    pid_plot.set_data([],[])
    p_slider_widget.set_val(.3)
    i_slider_widget.set_val(.01)
    d_slider_widget.set_val(.05)
    help_text_box.set_visible(True)
    help_text_box.set_text(data["err"])
    figure.canvas.draw()



pid = PID()
reference_point = 1
data = {
    "help" : "1)Left click on tools to use the tool.2)Right click on a point the in graph region to follow that amplitude.\n3)Use the sliders to set different values.4)Click on the particular P, I, D checkbox to activate or deactivate it.\n5)Left click on this box to hide it.",
    "err" : "The set P,I,D values doesn't converge. Try changing the values.\nLeft click on this box to hide it."
}


figure = plt.figure()
axes = figure.add_subplot()
axes.set_title("PID Grapher")
axes.set_xlim(0, 100)
axes.set_ylim(-100, 100)

pid_plot, = axes.plot([],[],"-r")
pid_plot.set_label("PID")
reference_plot, = axes.plot([],[],"-")
reference_plot.set_label("Input")
axes.legend()

check_box_axes = figure.add_subplot()
check_box_axes.set_position([.91, 0.75, 0.06, 0.09])
check_box = CheckButtons(check_box_axes, ["P", "I", "D"], [[.1, 0.01, 0.08, 0.08],[.1, 0.04, 0.08, 0.08],[.1, 0.07, 0.08, 0.08]])

p_slider_axes = figure.add_subplot()
p_slider_axes.set_position([.91, 0.3, 0.01, 0.4])
p_slider_widget = Slider(p_slider_axes, "P",0, 2, .3, orientation="vertical")

i_slider_axes = figure.add_subplot()
i_slider_axes.set_position([.94, 0.3, 0.01, 0.4])
i_slider_widget = Slider(i_slider_axes, "I",0, 2, .01,orientation="vertical")

d_slider_axes = figure.add_subplot()
d_slider_axes.set_position([.97, 0.3, 0.01, 0.4])
d_slider_widget = Slider(d_slider_axes, "D",0, 2, .05,orientation="vertical")

help_text_box = axes.text(0.4,0.02,"", color="white", transform=figure.transFigure, wrap=True, visible=True)
help_text_box.set_text(data["help"])
help_text_box.set_bbox(dict(facecolor='black', alpha=1))

axes.figure.canvas.mpl_connect("button_press_event", get_reference_point)
check_box.on_clicked(check_box_state)
p_slider_widget.on_changed(p_slider)
i_slider_widget.on_changed(i_slider)
d_slider_widget.on_changed(d_slider)
help_text_box.figure.canvas.mpl_connect("button_release_event", hide_text_box)

plt.show()