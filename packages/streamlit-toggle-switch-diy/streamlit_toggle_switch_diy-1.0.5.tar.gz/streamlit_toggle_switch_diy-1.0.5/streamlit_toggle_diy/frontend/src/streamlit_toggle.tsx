import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { useEffect, useRef } from "react";
import { createTheme } from "@material-ui/core/styles";
import { Typography, Switch, Grid } from "@material-ui/core";
import { ThemeProvider } from "@material-ui/styles";

interface ToggleSwitchProps {
  default_value: boolean;
  label_start?: string;
  label_end?: string;
  justify?: 'flex-start' | 'center' | 'flex-end';
  active_color?: string;
  inactive_color?: string;
  track_color?: string;
  label_bg_color_start?: string;
  label_bg_color_end?: string;
  background_color_near_button_start?: string;
  background_color_near_button_end?: string;
  border_radius?: string;
}

const StreamlitToggle = (props: ComponentProps) => {
  const {
    default_value,
    label_end,
    label_start,
    justify = 'flex-start',
    active_color = "#11567f",
    inactive_color = '#D3D3D3',
    track_color = "#29B5E8",
    label_bg_color_start,
    label_bg_color_end,
    background_color_near_button_start,
    background_color_near_button_end,
    border_radius = "8px",
  } = props.args as ToggleSwitchProps;

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    console.log("Setting frame height");
    Streamlit.setFrameHeight();

    // 如果需要动态监听变化，可以启用以下代码
    /*
    const resizeObserver = new ResizeObserver(() => {
      Streamlit.setFrameHeight();
    });

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => {
      resizeObserver.disconnect();
    };
    */
  }, []);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log("Toggle clicked:", event.target.checked);
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
          color: inactive_color,
        },
        colorSecondary: {
          "&$checked": {
            color: active_color,
          },
        },
        track: {
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

  const labelStartStyle = {
    backgroundColor: label_bg_color_start || "#6e6abb",
    color: "#7f1916",
    padding: "4px 8px",
    borderRadius: border_radius,
    display: "inline-block",
    fontWeight: "bold",
  };

  const labelEndStyle = {
    backgroundColor: label_bg_color_end || "#0F1C2E",
    color: "#FFFFFF",
    padding: "4px 8px",
    borderRadius: border_radius,
    display: "inline-block",
    fontWeight: "bold",
  };

  const buttonBackgroundStyle = {
    background: background_color_near_button_start && background_color_near_button_end
      ? `linear-gradient(to right, ${background_color_near_button_start}, ${background_color_near_button_end})`
      : background_color_near_button_start || background_color_near_button_end || "#ffffff",
    padding: "10px",
    borderRadius: border_radius,
    display: "flex",
    alignItems: "center",
  };

  return (
    <ThemeProvider theme={snowflakeTheme}>
      <Typography component="div" variant="subtitle1" paragraph={false} gutterBottom={false}>
        <div ref={containerRef} style={buttonBackgroundStyle}>
          <Grid
            container
            justifyContent={justify}
            alignItems="center"
            spacing={1}
          >
            {label_start && (
              <Grid item>
                <span style={labelStartStyle}>{label_start}</span>
              </Grid>
            )}
            <Grid item>
              <Switch
                checked={state.checkStatus}
                onChange={handleChange}
                name="checkStatus"
              />
            </Grid>
            {label_end && (
              <Grid item>
                <span style={labelEndStyle}>{label_end}</span>
              </Grid>
            )}
          </Grid>
        </div>
      </Typography>
    </ThemeProvider>
  );
};

export default withStreamlitConnection(StreamlitToggle);
