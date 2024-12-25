import { useEffect, useState } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { alpha, darken, lighten } from '@mui/material/styles';

// Remove the generateTonalPalette function as we'll use MUI's built-in color generation

const isPaletteColor = (color) => {
  return typeof color === 'string' && color.includes('.');
};

const getPaletteColor = (theme, colorString) => {
  if (!isPaletteColor(colorString)) return colorString;
  
  const [palette, shade] = colorString.split('.');
  const paletteObj = theme.palette[palette];
  
  if (!paletteObj) return colorString;
  return paletteObj[shade] || colorString;
};

const generateColorShades = (mainColor, isSecondary = false) => {
  const shades = {};
  
  // Generate shades from 100 to 900
  for (let i = 1; i <= 9; i++) {
    const shade = i * 100;
    if (i < 5) {
      // Lighter shades
      shades[shade] = isSecondary 
        ? lighten(mainColor, (5-i) * 0.15)
        : alpha(mainColor, 0.2 + (i * 0.15));
    } else {
      // Darker shades
      shades[shade] = isSecondary
        ? darken(mainColor, (i-5) * 0.1)
        : alpha(mainColor, 0.5 + ((i-5) * 0.1));
    }
  }
  
  return shades;
};

const generateSecondaryColor = (primaryColor) => {
  // Create a complementary color by adjusting hue and saturation
  const color = createTheme().palette.augmentColor({ color: { main: primaryColor } });
  return darken(color.dark, 0.1); // Use a slightly darker version for better contrast
};

const ElementsTheme = ({ children, theme }) => {
  const [elementsTheme, setElementsTheme] = useState(createTheme({
    components: {
      MuiPaper: {
        defaultProps: {
          elevation: 0,
          variant: "outlined",
          square: true
        },
        styleOverrides: {
          root: {
            backgroundImage: 'none',
            boxShadow: 'none !important',
            border: 'none',
            '&.MuiCard-root': {
              boxShadow: 'none !important',
              backgroundImage: 'none',
              border: 'none'
            }
          }
        }
      },
      MuiCard: {
        defaultProps: {
          elevation: 0,
          variant: "outlined",
          square: true
        },
        styleOverrides: {
          root: {
            backgroundImage: 'none',
            boxShadow: 'none !important',
            border: 'none',
            '&::before': {
              boxShadow: 'none'
            },
            '&::after': {
              boxShadow: 'none'
            }
          }
        }
      }
    }
  }));

  useEffect(() => {
    if (theme !== undefined) {
      const primaryShades = generateColorShades(theme.primaryColor);
      const secondaryColor = generateSecondaryColor(theme.primaryColor);
      const secondaryShades = generateColorShades(secondaryColor, true);
      
      const newTheme = createTheme({
        palette: {
          mode: theme.base,
          primary: {
            main: theme.primaryColor,
            ...primaryShades, // Add all shades
            light: primaryShades[300],
            dark: primaryShades[700],
          },
          secondary: {
            main: secondaryColor,
            ...secondaryShades,
            light: secondaryShades[300],
            dark: secondaryShades[700],
          },
          background: {
            default: theme.backgroundColor,
            paper: theme.secondaryBackgroundColor,
          },
          text: {
            primary: theme.textColor,
            secondary: theme.fadedText60,
          },
        },
        typography: {
          fontFamily: theme.font,
        },
        components: {
          MuiPaper: {
            defaultProps: {
              elevation: 0,
              variant: "outlined",
              square: true
            },
            styleOverrides: {
              root: {
                backgroundImage: 'none',
                boxShadow: 'none !important',
                border: 'none',
                '&.MuiCard-root': {
                  boxShadow: 'none !important',
                  backgroundImage: 'none',
                  border: 'none'
                },
                '& .plot-container': {
                  backgroundColor: 'transparent !important'
                }
              }
            }
          },
          MuiCard: {
            defaultProps: {
              elevation: 0,
              variant: "outlined",
              square: true
            },
            styleOverrides: {
              root: {
                backgroundImage: 'none',
                boxShadow: 'none !important',
                border: 'none',
                '&::before': {
                  boxShadow: 'none'
                },
                '&::after': {
                  boxShadow: 'none'
                }
              }
            }
          }
        }
      });

      setElementsTheme(newTheme);
    }
  }, [theme]);

  return <ThemeProvider theme={elementsTheme}>{children}</ThemeProvider>;
};

export default ElementsTheme;
