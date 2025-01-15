import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {
    Avatar,
    CircularProgress, ExpansionPanel, ExpansionPanelDetails,
    ExpansionPanelSummary,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
    Typography,
    withStyles
} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {localSettings} from "../../utils/localSettings.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";
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

function LocalSettingsPage(props) {
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [key, setKey] = useState("locale");
    const {classes, theme} = props;

    const [paramLocale, setParamLocale]
        = useState(localSettings.getStr("locale"));

    return (
        <div className="dj-container">
            <Typography variant="display3" style={{marginBottom: 16}}>
                Local settings
            </Typography>
            <Typography variant="caption">Please note that these settings are stored locally
            in your browser and therefore are not synchronized with other devices</Typography>
            <VWhitespace/>
            <ExpansionPanel expanded={key === 'locale'} onChange={() => setKey("locale")}>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                    <Typography className={classes.heading}>Locale</Typography>
                    <Typography className={classes.secondaryHeading}>Language and display</Typography>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails style={{alignItems: "center"}}>
                    <FormControl className={classes.formControl}>
                    <InputLabel htmlFor="param-locale">Locale</InputLabel>
                    <Select
                        defaultValue="en"
                        value={paramLocale}
                        onChange={e => {
                            setParamLocale(e.target.value);
                            localSettings.setStr("locale", e.target.value);
                        }}
                        inputProps={{
                            name: 'locale',
                            id: 'param-locale',
                        }}>
                        <MenuItem value="en">English</MenuItem>
                        <MenuItem value="ru">Russian</MenuItem>
                    </Select>
                </FormControl>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        </div>
    );
}

export default withStyles(styles, { withTheme: true })(LocalSettingsPage);
