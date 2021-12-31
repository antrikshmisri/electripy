import React from "react";

const Paragraph = ({
  text,
  style,
  children,
  id,
  className,
}) => {
  return (
    <p
      id={id}
      className={className}
      style={style}
    >
      {text}
      {children}
    </p>
  );
};

export default Paragraph;
