import React, { useState, useEffect, useRef } from "react";
import { eel } from "../eel";

import { convertColor } from "../utils/colorConversions";
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
    darker: "",
  });
  const [pressed, setPressed] = useState(false);

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
      darker: `rgb(${darkenedColor[0] * darkFactor}, ${
        darkenedColor[1] * darkFactor
      }, ${darkenedColor[2] * darkFactor})`,
    });
  }, []);

  return (
    <button
      onClick={(e) => {
        onClick ? onClick(e) : eel[`${id}_onClick_callback`](e);
      }}
      onMouseDown={() => {
        setPressed(true);
        iconContainerRef.current.style.backgroundColor = backgroundColor.darker;
        setStyleSheet({
          ...styleSheet,
          outline: `3px solid ${backgroundColor.dark
            .replace("(", ", 1)")
            .replace("rgb", "rgba")}`,
        });
      }}
      onMouseUp={() => {
        setPressed(false);
        iconContainerRef.current.style.backgroundColor = backgroundColor.dark;
      }}
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
      className={`${className} ${pressed ? "pressed" : "idle"}`}
    >
      {children.map((child, _) => {
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
