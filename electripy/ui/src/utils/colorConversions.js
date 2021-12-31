import colorMap from "../constants/colorMap";

const hexToRgb = (hex) => {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
};

const rgbToHex = (rgb) => {
  // https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
  const componentToHex = (component) => {
    var hex = component.toString(16);
    return hex.length === 1 ? "0" + hex : hex;
  };
  var colors = rgb.split("rgb").replace("(", "").replace(")", "").split(",");
  var hex = "#";

  hex += componentToHex(parseInt(colors[0], 16));
  hex += componentToHex(parseInt(colors[1], 16));
  hex += componentToHex(parseInt(colors[2], 16));

  return hex;
};

const isColorValid = (color) => {
  if (color in colorMap) {
    return true;
  }
  if (color.startsWith("rgb")) {
    return true;
  }
  if (color.startsWith("#") && color.length === 7) {
    return true;
  }
  return false;
};

export { hexToRgb, rgbToHex, isColorValid };
