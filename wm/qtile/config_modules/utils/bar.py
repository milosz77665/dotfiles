# from ..widgets.widgets import get_detailed_widget_list
# from ..variables import IS_DETAILED_BAR_VISIBLE


# def switch_bar(qtile):
#     global IS_DETAILED_BAR_VISIBLE
#     screen = qtile.current_screen
#     bar = screen.top

#     for widget in bar.widgets:
#         widget.finalize()

#     if IS_DETAILED_BAR_VISIBLE:
#         bar.widgets = minimal_widget_list
#         IS_DETAILED_BAR_VISIBLE = False
#     else:
#         bar.widgets = detailed_widget_list
#         IS_DETAILED_BAR_VISIBLE = True

#     for w in bar.widgets:
#         w._configure(qtile, bar)


#     bar._resize(bar.size, bar.widgets)
#     bar.draw()


# def switch_bar(qtile):
#     global IS_DETAILED_BAR_VISIBLE
#     screen = qtile.current_screen
#     bar = screen.top

#     for widget in bar.widgets:
#         try:
#             widget.finalize()
#         except Exception:
#             pass

#     if IS_DETAILED_BAR_VISIBLE:
#         bar.widgets = get_minimal_widget_list()
#         IS_DETAILED_BAR_VISIBLE = False
#     else:
#         bar.widgets = get_detailed_widget_list()
#         IS_DETAILED_BAR_VISIBLE = True

#     for w in bar.widgets:
#         if hasattr(w, "_configure"):
#             w._configure(qtile, bar)

#     bar.draw()


# def get_current_widget_list():
#     return (
#         get_detailed_widget_list()
#         if IS_DETAILED_BAR_VISIBLE
#         else get_minimal_widget_list()
#     )
