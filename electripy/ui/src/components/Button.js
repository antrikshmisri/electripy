import React, { useState, useEffect, useRef } from "react";
import { eel } from "../eel";

import colorMap from "../constants/colorMap";
import { hexToRgb } from "../utils/colorConversions";
import Paragraph from "./Paragraph";
import Image from "./Image";

const Button = ({
  style,
  children,
  id,
  className,
  onClick = null,
  darkFactor = 0.8,
}) => {
  const [styleSheet, setStyleSheet] = useState(style || {});
  const [backgroundColor, setBackgroundColor] = useState({
    normal: "",
    dark: "",
  });
  const iconContainerRef = useRef(null);
  const textContainerRef = useRef(null);

  useEffect(() => {
    if (!("backgroundColor" in styleSheet)) {
      setStyleSheet({ ...styleSheet, backgroundColor: "#ffffff" });
    }

    var currentColor = convertColor(styleSheet.backgroundColor, true);

    var darkenedColor = [
      Math.floor(currentColor.r * darkFactor),
      Math.floor(currentColor.g * darkFactor),
      Math.floor(currentColor.b * darkFactor),
    ];

    setBackgroundColor({
      normal: styleSheet.backgroundColor,
      dark: `rgb(${darkenedColor[0]}, ${darkenedColor[1]}, ${darkenedColor[2]})`,
    });
  }, []);

  const convertColor = (color, asObject = false) => {
    if (colorMap[color]) {
      color = colorMap[color];
    }

    if (!color.startsWith("rgb")) {
      color = hexToRgb(color);
      if (asObject) {
        return color;
      }

      color = `rgb(${color.r}, ${color.g}, ${color.b})`;
      return color;
    } else {
      if (asObject) {
        color = color
          .replace("rgb", "")
          .replace("(", "")
          .replace(")", "")
          .split(",");
        return {
          r: parseInt(color[0], 10),
          g: parseInt(color[1], 10),
          b: parseInt(color[2], 10),
        };
      }
      return color;
    }
  };

  return (
    <button
      onClick={onClick || eel[`${id}_onClick_callback`]}
      onMouseEnter={() => {
        iconContainerRef.current.style.width = "100%";
        setStyleSheet({
          ...styleSheet,
          backgroundColor: backgroundColor.dark,
        });
      }}
      onMouseLeave={() => {
        iconContainerRef.current.style.width = "50px";
        setStyleSheet({
          ...styleSheet,
          backgroundColor: backgroundColor.normal,
        });
      }}
      style={styleSheet}
      id={id}
      className={className}
    >
      {children.map((child, idx) => {
        const { className, ...props } = child.props;

        switch (child.type) {
          case Paragraph:
            if (className === "btn-text") {
              return (
                <div className="text-container" ref={textContainerRef}>
                  <Paragraph className="btn-text" {...props} key={props.id} />
                </div>
              );
            }
            return <Paragraph {...child.props} key={props.id} />;

          case Image:
            if (className === "btn-logo") {
              return (
                <div
                  className="icon-container"
                  style={{ background: backgroundColor.dark }}
                  ref={iconContainerRef}
                >
                  <Image className="btn-logo" {...props} key={props.id} />
                </div>
              );
            }
            return <Image {...child.props} key={props.id} />;

          default:
            return child;
        }
      })}
    </button>
  );
};

export default Button;
