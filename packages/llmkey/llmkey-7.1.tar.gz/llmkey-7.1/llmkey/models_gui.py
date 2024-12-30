import tkinter as tk

from . import tk_tools

def models_gui(parent, model_names, disabled, callback):
    window = tk.Toplevel()

    model_vars = {name: tk.IntVar() for name in model_names}
    for name, var in model_vars.items():
        var.set(name not in model_names)

    for name in model_names:
        tk.Checkbutton(window, text=name, variable=model_vars[name]).pack(anchor=tk.W, padx=20)

    ok_cancel = tk.Frame(window, borderwidth=25)
    ok = tk.Button(ok_cancel, text="OK")
    ok.pack(side=tk.LEFT, padx=5)
    cancel = tk.Button(ok_cancel, text="Cancel")
    cancel.pack(side=tk.LEFT, padx=5)
    ok_cancel.pack()

    window.wait_visibility()
    window.grab_set()

    def accept(*_):
        m = model_vars
        window.grab_release()
        window.destroy()
        disabled = [k for k, v in model_vars.items() if v.get() == 0]
        callback(disabled)

    tk_tools.bind_click(ok, accept)




if __name__ == '__main__':
    root = tk.Tk()
    models_gui(root, ["one", "two", "three"], ["one"], print)
    root.mainloop()
