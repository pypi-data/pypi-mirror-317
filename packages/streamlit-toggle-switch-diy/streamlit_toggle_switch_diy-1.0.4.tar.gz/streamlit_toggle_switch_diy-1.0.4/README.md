# streamlit_toggle_switch_diy

Creates a toggle switch with color and placement customizations, and you can change the label's color.

## Installation

```shell
pip install streamlit-toggle-switch-diy==1.0.4
```

## Usage

```python
import streamlit as st
import streamlit_toggle_diy as tog

tog.st_toggle_switch(   label=None,
                        key=None,
                        default_value=False,
                        label_after=False,
                        inactive_color='#D3D3D3',
                        active_color="#11567f",
                        track_color="#29B5E8",
                        label_bg_color_start=None,  
                        label_bg_color_end=None,  
                        background_color_near_button_start=None,  
                        background_color_near_button_end=None  
                     )
```
