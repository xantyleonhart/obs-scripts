import obspython as S

interval    = 80
source_name = ""
source_wid = ""
description = "Enables/Disables window capture source when the window gets/loses focus"

# ------------------------------------------------------------

import Xlib
import Xlib.display

disp = Xlib.display.Display()
root = disp.screen().root
last_seen = {'xid': None}

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')

#returns window_id of the new window when changing windows, -1 otherwise
def isfocused():
    window_id = root.get_full_property(NET_ACTIVE_WINDOW,
                                       Xlib.X.AnyPropertyType).value[0]
    if(window_id!=last_seen['xid']):
        last_seen['xid']=window_id
        return window_id
    return -1

#enable source if its window is focused, disable otherwise
def update_window():
    wn=isfocused()
    if(wn > -1 and source_wid != ""):
        source=S.obs_get_source_by_name(source_name)
        if(wn == int(source_wid)):
            # print('show: ',int(source_wid))
            S.obs_source_set_enabled(source,True)
        else:
            # print('hide: ',int(source_wid))
            S.obs_source_set_enabled(source,False)
        S.obs_source_release(source)

#Update source info (window id)
def update_source(calldata=None): 
    global source_wid
    #Get source by name
    source = S.obs_get_source_by_name(source_name)
    #Get window properties from the source (window id)
    props = S.obs_source_get_settings(source)
    source_wid = S.obs_data_get_string(props,"capture_window").split('\r')[0]
    print("updated source: ",source_wid)
    print(S.obs_data_get_string(props,"capture_window"))
    # print(last_seen)
    S.obs_source_release(source)

# ------------------------------------------------------------

def script_description():
    return description


# Called each time script properties are modified
def script_update(settings):
    global interval
    global source_name
    global s_handler
    global source_wid
    
    #disconnect callbacks from old source
    disconnect_callbacks()

    #Set old source visible
    source = S.obs_get_source_by_name(source_name)
    S.obs_source_set_enabled(source,True)
    S.obs_source_release(source)


    # Update variables with the new property values
    interval    = S.obs_data_get_int(settings, "interval")
    source_name = S.obs_data_get_string(settings, "source")
    
    #connect callbacks to new source
    connect_callbacks()
    update_source()

    # Crear/Actualizar un timer que lanza una funcion periodicamente
    S.timer_remove(update_window)
    S.timer_add(update_window, interval)

def script_defaults(settings):
    S.obs_data_set_default_int(settings, "interval", 80)

# Definition of script properties to be shown on the GUI
def script_properties():
    props = S.obs_properties_create()
 
    S.obs_properties_add_int(props, "interval", "Latency (ms)", 5, 3600, 1)

    p = S.obs_properties_add_list(props, "source", "Video Source", S.OBS_COMBO_TYPE_EDITABLE, S.OBS_COMBO_FORMAT_STRING)
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            if source_id == "xcomposite_input":
                name = S.obs_source_get_name(source)
                #---- debug:show source type ----#
                # name += '('+source_id+')'
                S.obs_property_list_add_string(p, name, name)

        S.source_list_release(sources)

    return props


##Callbacks--------------------------------------------------------------------------

def connect_callbacks():
    print("binding to "+source_name)
    source = S.obs_get_source_by_name(source_name)
    sh = S.obs_source_get_signal_handler(source)
    S.signal_handler_connect(sh, "save", update_source)
    S.signal_handler_connect_global(sh, onActivate)
    S.obs_source_release(source)

def disconnect_callbacks():
    print("unbinding to "+source_name)
    source = S.obs_get_source_by_name(source_name)
    sh = S.obs_source_get_signal_handler(source)
    S.signal_handler_disconnect(sh, "save", update_source)
    S.signal_handler_connect_global(sh, onActivate)
    S.obs_source_release(source)

# Debug events
# def onActivate(e,calldata):
#     # source = S.calldata_source(calldata,"source")
#     print(e)

# def onDeactivate(calldata):
#     # source = S.calldata_source(calldata,"source")
#     print('\n deactivated')


# Subscribe on_load callback
def script_load(settings):
    S.obs_frontend_add_event_callback(on_load)

# Waits until frontend is loaded to get source data. Otherwise it can get empty reference.
def on_load(event):
    if event == S.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        connect_callbacks()
        update_source()


