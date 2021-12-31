import React from "react";

const Image = ({ src, alt, size, style, children, id, className }) => {
  return (
    <img
      src={src}
      style={style}
      alt={alt}
      width={size[0]}
      height={size[1]}
      id={id}
      className={className}
    >
      {children}
    </img>
  );
};

export default Image