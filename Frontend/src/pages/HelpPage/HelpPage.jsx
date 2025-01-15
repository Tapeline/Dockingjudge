import React, {useState} from "react";
import {useNavigate} from "react-router-dom";
import {
    CircularProgress, ExpansionPanel, ExpansionPanelDetails, ExpansionPanelSummary, FormControl, InputLabel, MenuItem,
    Paper, Select,
    Table,
    TableBody,
    TableCell, TableHead,
    TableRow,
    Typography,
    withStyles
} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import locales from "../../locales.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";
import {localSettings} from "../../utils/localSettings.jsx";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

const styles = theme => ({
    root: {
        width: '100%',
      },
      heading: {
        fontSize: theme.typography.pxToRem(15),
        flexBasis: '33.33%',
        flexShrink: 0,
        marginRight: "1rem"
      },
      secondaryHeading: {
        fontSize: theme.typography.pxToRem(15),
        color: theme.palette.text.secondary,
      },
});

function HelpPage(props) {
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [key, setKey] = useState("verdicts");
    const {classes, theme} = props;

    return (
        <div className="dj-container">
            <Typography variant="display3" style={{marginBottom: 16}}>
                {locales.helpPage.title}
            </Typography>
            <VWhitespace/>
            <ExpansionPanel expanded={key === 'verdicts'} onChange={() => setKey("verdicts")}>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                    <Typography className={classes.heading}>{locales.helpPage.titleVerdicts}</Typography>
                    <Typography className={classes.secondaryHeading}>{locales.helpPage.subtitleVerdicts}</Typography>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails style={{alignItems: "center", padding: 0, overflowX: "scroll"}}>
                    <Table className={classes.table}>
                        <TableBody>
                            <TableRow>
                                <TableCell component="th" scope="column" style={{width: "5%"}}>
                                    {locales.helpPage.columnCode}</TableCell>
                                <TableCell component="th" scope="column">
                                    {locales.helpPage.columnShort}</TableCell>
                                <TableCell component="th" scope="column" style={{width: "50%"}}>
                                    {locales.helpPage.columnDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>NC</code></TableCell>
                                <TableCell>{locales.helpPage.verdictNCShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictNCDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>OK</code></TableCell>
                                <TableCell>{locales.helpPage.verdictOKShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictOKDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>WA</code></TableCell>
                                <TableCell>{locales.helpPage.verdictWAShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictWADesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>RE</code></TableCell>
                                <TableCell>{locales.helpPage.verdictREShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictREDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>PE</code></TableCell>
                                <TableCell>{locales.helpPage.verdictPEShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictPEDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>PCF</code></TableCell>
                                <TableCell>{locales.helpPage.verdictPCFShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictPCFDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>TL</code></TableCell>
                                <TableCell>{locales.helpPage.verdictTLShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictTLDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>ML</code></TableCell>
                                <TableCell>{locales.helpPage.verdictMLShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictMLDesc}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row"><code>TSF</code></TableCell>
                                <TableCell>{locales.helpPage.verdictTSFShort}</TableCell>
                                <TableCell>{locales.helpPage.verdictTSFDesc}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        </div>
    );
}

export default withStyles(styles, { withTheme: true })(HelpPage);
