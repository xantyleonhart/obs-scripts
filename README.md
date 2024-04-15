# obs-scripts

## hidewindow
  - hidewindow-xlib.py

    A simple script using X11 (Xlib) that enables or disables a window capture source whenever it gains or loses focus. 
    May be useful to hide the window when Alt+tabbing to show a background image or multimedia source underneath it.
    Can be easily tweaked to automatically swap between scenes as well.
  - hidewindow-win32.py

    Tweaked verison of `hidewindow-xlib.py`, using win32gui libary (which can be installed by `pip install pywin32`).
    Made by `sheriffoftiltover` on the OBS Fourms.
    
    Thread : https://obsproject.com/forum/threads/how-to-set-window-capture-to-hide-when-window-is-minimized.108569/
    
    Gist : https://gist.githubusercontent.com/sheriffoftiltover/110b06ed9caa16d44ccd1884912aef28/raw/301df1e2b50b84e079da3dd84878c2269e7a003a/hide_unfocused_windows.py
