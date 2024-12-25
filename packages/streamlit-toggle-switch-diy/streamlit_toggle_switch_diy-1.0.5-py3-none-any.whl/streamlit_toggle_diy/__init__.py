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
        key=None,
        label_start="",  # 默认空字符串
        label_end="",    # 默认空字符串
        justify='flex-start',
        default_value=False,
        inactive_color='#D3D3D3',
        active_color="#11567f",
        track_color="#29B5E8",
        label_bg_color_start=None,
        label_bg_color_end=None,
        background_color_near_button_start=None,
        background_color_near_button_end=None,
        border_radius=None,
):
    toggle_value = _component_func(
        key=key,
        default_value=default_value,
        label_start=label_start,
        label_end=label_end,
        justify=justify,
        inactive_color=inactive_color,
        active_color=active_color,
        track_color=track_color,
        label_bg_color_start=label_bg_color_start,
        label_bg_color_end=label_bg_color_end,
        background_color_near_button_start=background_color_near_button_start,
        background_color_near_button_end=background_color_near_button_end,
        border_radius=border_radius,
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

    # 新增圆角选择器
    border_radius = st.text_input('选择组件圆角（如：4px, 8px, 50%）', '8px')

    # 新增对齐方式选择器
    justify = st.selectbox(
        '选择标签和开关的对齐方式',
        ('flex-start', 'center', 'flex-end')
    )

    columns = st.columns(3)
    with columns[0]:
        st_toggle_switch(
            key='c1',
            label_start="Question 1",
            label_end="",  # 不显示后标签
            justify=justify,
            default_value=True,
            inactive_color='#D3D3D3',
            active_color="#11567f",
            track_color="#29B5E8",
            label_bg_color_start=color1_start,
            label_bg_color_end=color1_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end,
            border_radius=border_radius,
        )
        st_toggle_switch(
            key='c2',
            label_start="Question 2",
            label_end="",  # 不显示后标签
            justify=justify,
            default_value=False,
            inactive_color='#B0C4DE',
            active_color="#1E90FF",
            track_color="#87CEFA",
            label_bg_color_start=color2_start,
            label_bg_color_end=color2_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end,
            border_radius=border_radius,
        )
    with columns[1]:
        st_toggle_switch(
            key='q2',
            label_start="",  # 不显示前标签
            label_end="Question 3",
            justify=justify,
            default_value=True,
            inactive_color='#DDA0DD',
            active_color="#9400D3",
            track_color="#BA55D3",
            label_bg_color_start=color3_start,
            label_bg_color_end=color3_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end,
            border_radius=border_radius,
        )
        st_toggle_switch(
            key='q3',
            label_start="",  # 不显示前标签
            label_end="Question 4",
            justify=justify,
            default_value=False,
            inactive_color='#FFA07A',
            active_color="#FF4500",
            track_color="#FF6347",
            label_bg_color_start=color4_start,
            label_bg_color_end=color4_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end,
            border_radius=border_radius,
        )
    with columns[2]:
        st_toggle_switch(
            key='q1',
            label_start="Disable Filter",
            label_end="",  # 不显示后标签
            justify=justify,
            default_value=True,
            inactive_color='#98FB98',
            active_color="#00FF7F",
            track_color="#00FA9A",
            label_bg_color_start=color5_start,
            label_bg_color_end=color5_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end,
            border_radius=border_radius,
        )
        range_slider_toggle = st_toggle_switch(
            key='ql',
            label_start="Disable Filter",
            label_end="",  # 不显示后标签
            justify=justify,
            default_value=True,
            inactive_color='#98FB98',
            active_color="#00FF7F",
            track_color="#00FA9A",
            label_bg_color_start=color5_start,
            label_bg_color_end=color5_end,
            background_color_near_button_start=button_bg_start,
            background_color_near_button_end=button_bg_end,
            border_radius=border_radius,
        )
        range_slider = st.slider(
            label="Filter Range",
            min_value=0,
            max_value=100,
            disabled=range_slider_toggle
        )