import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { useEffect } from "react";
import { createTheme } from "@material-ui/core/styles";
import { Typography, Switch, Grid } from "@material-ui/core";
import { ThemeProvider } from "@material-ui/styles";
// 如果有自定义 CSS 文件，可以在这里导入
// import './streamlit_toggle_diy.css';

const StreamlitToggle = (props: ComponentProps) => {
  const {
    default_value,
    label_end,
    label_start,
    justify,
    active_color,
    inactive_color,
    track_color,
    label_bg_color_start,
    label_bg_color_end,
    background_color_near_button_start, // 新增参数
    background_color_near_button_end,   // 新增参数
  } = props.args;

  useEffect(() => Streamlit.setFrameHeight());

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    Streamlit.setComponentValue(event.target.checked);
  };

  const [state, setState] = React.useState({
    checkStatus: default_value,
  });

  const snowflakeTheme = createTheme({
    overrides: {
      MuiSwitch: {
        switchBase: {
          // 控制滑块未激活时的颜色
          color: inactive_color,
        },
        colorSecondary: {
          "&$checked": {
            // 控制滑块激活时的颜色
            color: active_color,
          },
        },
        track: {
          // 控制轨道未激活时的颜色
          opacity: 0.1,
          backgroundColor: track_color,
          "$checked$checked + &": {
            opacity: 1,
            backgroundColor: track_color,
          },
        },
      },
    },
  });

  // 定义动态标签样式，使用传入的背景颜色参数
  const labelStartStyle = {
    backgroundColor: label_bg_color_start || "#6e6abb", // 如果未传入，使用默认颜色
    color: "#7f1916",
    padding: "4px 8px",
    borderRadius: "4px",
    display: "inline-block",
    fontWeight: "bold",
  };

  const labelEndStyle = {
    backgroundColor: label_bg_color_end || "#0F1C2E", // 如果未传入，使用默认颜色
    color: "#FFFFFF",
    padding: "4px 8px",
    borderRadius: "4px",
    display: "inline-block",
    fontWeight: "bold",
  };

  // 定义按钮附近背景样式
  const buttonBackgroundStartStyle = {
    backgroundColor: background_color_near_button_start || "#ffffff", // 默认白色
    padding: "10px",
    borderRadius: "8px",
    display: "flex",
    alignItems: "center",
  };

  const buttonBackgroundEndStyle = {
    backgroundColor: background_color_near_button_end || "#ffffff", // 默认白色
    padding: "10px",
    borderRadius: "8px",
    display: "flex",
    alignItems: "center",
  };

  return (
    <ThemeProvider theme={snowflakeTheme}>
      <Typography component="div" variant="subtitle1" paragraph={false} gutterBottom={false}>
        <Grid
          container
          justifyContent={justify}
          alignItems="center"
          spacing={1}
          style={
            background_color_near_button_start || background_color_near_button_end
              ? {
                  backgroundColor: background_color_near_button_start || background_color_near_button_end,
                  padding: "10px",
                  borderRadius: "8px",
                }
              : {}
          }
        >
          <Grid item>
            <span style={labelStartStyle}>{label_start}</span>
          </Grid>
          <Grid item>
            <Switch
              checked={state.checkStatus}
              onChange={handleChange}
              name="checkStatus"
            />
          </Grid>
          <Grid item>
            <span style={labelEndStyle}>{label_end}</span>
          </Grid>
        </Grid>
      </Typography>
    </ThemeProvider>
  );
};

export default withStreamlitConnection(StreamlitToggle);
