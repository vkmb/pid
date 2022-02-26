import matplotlib.pyplot as plt
from numpy import NaN, Inf
from matplotlib.widgets import Slider, CheckButtons
from simple_pid import PID


def update_pid_graph():
    global pid, reference_point, reference_plot, pid_plot, axes
    pid.follow(reference_point, 100)
    ref, out, err, timestep = pid.put_data()    
    out_min = min(out)
    out_max = max(out)
    ll_out = -20 + out_min if out_min < 0 else out_min + 20
    ul_out = -20 + out_max if out_max < 0 else out_max + 20

    # Out of bounds bug
    # print( ul_out is NaN, ul_out  is Inf)
    # if ll_out is NaN or ll_out is Inf or ul_out is NaN or ul_out  is Inf:
    #     axes.set_title("Data doesn't converget")
    #     return
    # if axes.get_title() != "PID Grapher":
    #     axes.set_title("PID Grapher")

    reference_plot.set_data(timestep, ref)
    pid_plot.set_data(timestep, out)
    axes.set_xlim(min(timestep), max(timestep)+.8)
    axes.set_ylim(ll_out, ul_out)
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
    reference_point = event.ydata
    update_pid_graph()
    


pid = PID()
reference_point = 1
figure = plt.figure()
axes = figure.add_subplot()
axes.set_title("PID Grapher")
axes.set_xlim(0, 100)
axes.set_ylim(-100, 100)

pid_plot, = axes.plot([],[],"-r")
reference_plot, = axes.plot([],[],"-")
cid = axes.figure.canvas.mpl_connect("button_release_event", get_reference_point)
reference_plot.set_label("PID")
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

check_box.on_clicked(check_box_state)
p_slider_widget.on_changed(p_slider)
i_slider_widget.on_changed(i_slider)
d_slider_widget.on_changed(d_slider)


plt.show()