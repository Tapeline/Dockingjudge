import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {
    CircularProgress,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableRow,
    Typography,
    withStyles
} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import locales from "../../locales.jsx";

const styles = theme => ({});

function HelpPage(props) {
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {classes, theme} = props;

    return (
        <div>
            <Typography variant="display2" style={{marginBottom: 16}}>
                {locales.helpPage.title}
            </Typography>
            <Typography variant="title">
                {locales.helpPage.titleVerdicts}
            </Typography>
            <Paper className={classes.root}>
                <Table className={classes.table}>
                    <TableBody>
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
            </Paper>
        </div>
    );
}

export default withStyles(styles, { withTheme: true })(HelpPage);
