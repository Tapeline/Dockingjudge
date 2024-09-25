import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {CircularProgress, FormControl, InputLabel, MenuItem, Select, Typography, withStyles} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {localSettings} from "../../utils/localSettings.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";

const styles = theme => ({});

function LocalSettingsPage(props) {
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {classes, theme} = props;
    const [paramLocale, setParamLocale]
        = useState(localSettings.getStr("locale"));

    return (
        <div>
            <Typography variant="display2" style={{marginBottom: 16}}>
                Local settings
            </Typography>
            <Typography variant="caption">Please note that these settings are stored locally
            in your browser and therefore are not synchronized with other devices</Typography>
            <VWhitespace/>
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
        </div>
    );
}

export default withStyles(styles, { withTheme: true })(LocalSettingsPage);
