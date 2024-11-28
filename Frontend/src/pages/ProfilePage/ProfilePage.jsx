import React, {useEffect, useState} from "react";
import {Button, Form, Tab, Tabs} from "react-bootstrap";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import {useNavigate, useParams} from "react-router-dom";
import {
    deleteProfile,
    getProfile, modifyProfileSettings, setUserProfilePic
} from "../../api/endpoints-accounts.jsx";
import ConfirmDeletionDialog from "../../components/Dialogs/ConfirmDeletionDialog/ConfirmDeletionDialog.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {
    Avatar,
    ExpansionPanel,
    ExpansionPanelDetails,
    ExpansionPanelSummary,
    Typography,
    withStyles
} from "@material-ui/core";
import locales from "../../locales.jsx";
import HWhitespace from "../../utils/HWhitespace.jsx";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

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

function ProfilePage(props) {
    const { classes } = props;
    const [key, setKey] = useState("general");
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [profileData, setProfileData] = useState(null);
    const [profilePic, setProfilePic] = useState();

    useEffect(() => {
        getProfile(accessToken).then(response => {
            setProfileData(response.data);
        });
    }, []);


    if (profileData === null)
        return <Preloader/>;

    const onAccountDelete = () => {
        deleteProfile(accessToken).then((response) => {
            if (!response.success) toastError(response.reason);
            else window.location.href = "/";
        });
    };

    return (<div className="dj-container">
        <Typography variant="display2" style={{marginBottom: 16}}>
            Your profile
        </Typography>
        <VWhitespace size={1}/>
        <ExpansionPanel expanded={key === 'general'} onChange={() => setKey("general")}>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                <Typography className={classes.heading}>Identification</Typography>
                <Typography className={classes.secondaryHeading}>Your personal data</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails style={{alignItems: "center"}}>
                <Typography>
                    <Avatar>{profileData.username[0]}</Avatar>
                </Typography>
                <HWhitespace/>
                <Typography variant="title">
                    {profileData.username}
                </Typography>
                <HWhitespace/>
                <Typography>id #{profileData.id}</Typography>
            </ExpansionPanelDetails>
        </ExpansionPanel>
        <ExpansionPanel expanded={key === 'danger'} onChange={() => setKey("danger")}>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                <Typography className={classes.heading}>Danger zone</Typography>
                <Typography className={classes.secondaryHeading}>
                    Dangerous actions that cannot be reverted</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                <ConfirmDeletionDialog
                        buttonText="Delete account"
                        header="Delete account?"
                        text={<>
                            Are you sure you want to delete your account?<br/>
                            <b>This action is not undoable, proceed with caution!</b>
                        </>}
                        onOk={onAccountDelete}
                    />
            </ExpansionPanelDetails>
        </ExpansionPanel>
    </div>);
}

export default withStyles(styles, { withTheme: true })(ProfilePage);
