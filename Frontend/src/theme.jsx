import { createMuiTheme } from '@material-ui/core/styles';

const theme = createMuiTheme({
  palette: {
    primary: {
      // light: will be calculated from palette.primary.main,
      main: '#2F24C1',
      // dark: will be calculated from palette.primary.main,
      // contrastText: will be calculated to contrast with palette.primary.main
    },
    secondary: {
      main: '#4D12EE',
      // dark: will be calculated from palette.secondary.main,
    },
    // error: will use the default color
  },
});

export default theme;