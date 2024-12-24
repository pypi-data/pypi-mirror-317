import os
import streamlit.components.v1 as components
import streamlit as st

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_toggle_diy",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_toggle_diy", path=build_dir)


def st_toggle_switch(
        label=None,
        key=None,
        default_value=False,
        label_after=False,
        inactive_color='#D3D3D3',
        active_color="#11567f",
        track_color="#29B5E8",
        label_bg_color_start=None,  # 新增参数
        label_bg_color_end=None,  # 新增参数
        background_color_near_button_start=None,  # 新增参数
        background_color_near_button_end=None  # 新增参数
):
    if label_after:
        label_end = label
        label_start = ''
        justify = 'flex-start'
    else:
        label_start = label
        label_end = ''
        justify = 'flex-start'
        # justify = 'flex-end'

    toggle_value = _component_func(
        key=key,
        default_value=default_value,
        label_after=label_after,
        label_start=label_start,
        label_end=label_end,
        justify=justify,
        inactive_color=inactive_color,
        active_color=active_color,
        track_color=track_color,
        label_bg_color_start=label_bg_color_start,  # 传递新增参数
        label_bg_color_end=label_bg_color_end,  # 传递新增参数
        background_color_near_button_start=background_color_near_button_start,  # 传递新增参数
        background_color_near_button_end=background_color_near_button_end  # 传递新增参数
    )
    return toggle_value if toggle_value is not None else default_value


if not _RELEASE:
    st.header('Streamlit Toggle Switch')
    st.write('---')

    # 使用 color_picker 选择颜色
    color1_start = st.color_picker('选择 Question 1 标签起始背景颜色', '#FFD700')
    color1_end = st.color_picker('选择 Question 1 标签结束背景颜色', '#FF8C00')

    color2_start = st.color_picker('选择 Question 2 标签起始背景颜色', '#ADFF2F')
    color2_end = st.color_picker('选择 Question 2 标签结束背景颜色', '#32CD32')

    color3_start = st.color_picker('选择 Question 3 标签起始背景颜色', '#1E90FF')
    color3_end = st.color_picker('选择 Question 3 标签结束背景颜色', '#0000FF')

    color4_start = st.color_picker('选择 Question 4 标签起始背景颜色', '#FF69B4')
    color4_end = st.color_picker('选择 Question 4 标签结束背景颜色', '#FF1493')

    color5_start = st.color_picker('选择 Disable Filter 标签起始背景颜色', '#00FA9A')
    color5_end = st.color_picker('选择 Disable Filter 标签结束背景颜色', '#00FF7F')

    # 新增颜色选择器用于按钮附近的背景颜色
    button_bg_start = st.color_picker('选择按钮附近的起始背景颜色', '#FFFFFF')
    button_bg_end = st.color_picker('选择按钮附近的结束背景颜色', '#FFFFFF')

    columns = st.columns(3)
    with columns[0]:
        st_toggle_switch(
            label="Question 1",
            key='c1',
            label_after=False,
            label_bg_color_start=color1_start,
            label_bg_color_end=color1_end,
            background_color_near_button_start=button_bg_start,  # 传递新增参数
            background_color_near_button_end=button_bg_end  # 传递新增参数
        )
        st_toggle_switch(
            label="Question 2",
            key='c2',
            label_after=False,
            label_bg_color_start=color2_start,
            label_bg_color_end=color2_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end
        )
    with columns[1]:
        st_toggle_switch(
            label="Question 3",
            key='q2',
            label_after=True,
            default_value=True,
            label_bg_color_start=color3_start,
            label_bg_color_end=color3_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end
        )
        st_toggle_switch(
            label="Question 4",
            key='q3',
            label_after=True,
            default_value=True,
            label_bg_color_start=color4_start,
            label_bg_color_end=color4_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end
        )
    with columns[2]:
        range_slider_toggle = st_toggle_switch(
            "Disable Filter",
            key='q1',
            label_after=False,
            default_value=True,
            label_bg_color_start=color5_start,
            label_bg_color_end=color5_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end
        )
        range_slider = st.slider(
            label="Filter Range",
            min_value=0,
            max_value=100,
            disabled=range_slider_toggle
        )
