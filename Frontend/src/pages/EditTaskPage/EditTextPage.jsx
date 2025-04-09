import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests, getContestPage, modifyQuizPage, modifyTextPage} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {
    Button,
    CircularProgress,
    FormControlLabel,
    Grid,
    Paper, Switch,
    TextField,
    Typography,
    withStyles
} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {Editor} from "@monaco-editor/react";
import {Save} from "@material-ui/icons";
import {lightGreen} from "@material-ui/core/colors";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";

const styles = theme => ({});

function EditTextPage(props) {
    const navigate = useNavigate();
    const {contestId, pageId} = useParams();
    const accessToken = localStorage.getItem("accessToken");
    const [pageData, setPageData] = useState(null);
    const {classes, theme} = props;

    const [pageTitle, setPageTitle] = useState(null);
    const [pageDescription, setPageDescription] = useState(null);
    const [isEnterPage, setIsEnterPage] = useState(null);

    useEffect(() => {
        getContestPage(accessToken, contestId, "text", pageId).then(response => {
            setPageData(response.data);
            setPageTitle(response.data.name);
            setPageDescription(response.data.text);
            setIsEnterPage(response.data.is_enter_page);
        });
    }, []);

    const applyChanges = () => {
        modifyTextPage(accessToken, contestId, pageId, {
            name: pageTitle,
            text: pageDescription,
            is_enter_page: isEnterPage
        }).then(response => {
            if (!response.success) {
                toastError(response.reason);
                return;
            }
            toastSuccess("Saved");
        })
    };

    return (
        pageData === null?
        <Preloader/>
        :
            <Paper style={{padding: "1rem", maxWidth: 1200}}>
                <Typography variant="headline">Edit text page</Typography>
                <VWhitespace/>
                <Button onClick={applyChanges} mini fullWidth
                        style={{marginBottom: 8}}
                        variant="raised">
                    <Save/>&nbsp;Save
                </Button>
                <TextField
                    id="title"
                    label="Title"
                    value={pageTitle}
                    onChange={e => setPageTitle(e.target.value)}
                    margin="normal"
                    fullWidth
                />
                <br/>
                <TextField
                    id="desc"
                    label="Description"
                    multiline
                    value={pageDescription}
                    onChange={e => setPageDescription(e.target.value)}
                    margin="normal"
                    fullWidth
                />
                <br/>
                <FormControlLabel
                    control={
                        <Switch
                            checked={isEnterPage}
                            onChange={e => setIsEnterPage(e.target.checked)}
                        />
                    }
                    label="Is enter page?"
                />
            </Paper>
    );
}

export default withStyles(styles, { withTheme: true })(EditTextPage);
