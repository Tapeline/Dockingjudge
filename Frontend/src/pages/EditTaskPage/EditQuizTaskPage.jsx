import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests, getContestPage, modifyQuizPage} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {Button, CircularProgress, Grid, Paper, TextField, Typography, withStyles} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {Editor} from "@monaco-editor/react";
import {Save} from "@material-ui/icons";
import {lightGreen} from "@material-ui/core/colors";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";

const styles = theme => ({});

function EditQuizTaskPage(props) {
    const navigate = useNavigate();
    const {contestId, pageId} = useParams();
    const accessToken = localStorage.getItem("accessToken");
    const [pageData, setPageData] = useState(null);
    const {classes, theme} = props;

    const [pageTitle, setPageTitle] = useState(null);
    const [pageDescription, setPageDescription] = useState(null);
    const [validatorJSON, setValidatorJSON] = useState(null);

    useEffect(() => {
        getContestPage(accessToken, contestId, "quiz", pageId).then(response => {
            setPageData(response.data);
            setPageTitle(response.data.title);
            setPageDescription(response.data.description);
            setValidatorJSON(JSON.stringify(response.data.validator, null, 2));
        });
    }, []);

    const applyChanges = () => {
        let validatorParsed;
        try {
            validatorParsed = JSON.parse(validatorJSON);
        } catch (err) {
            toastError(err.toString());
            return;
        }
        modifyQuizPage(accessToken, contestId, pageId, {
            title: pageTitle,
            description: pageDescription,
            validator: validatorParsed
        }).then(response => {
            if (!response.success) {
                toastError(response.reason);
                return;
            }
            toastSuccess("Saved");
        })
    };

    return (
        pageData === null || validatorJSON === null?
        <CircularProgress className={classes.progress}/>
        :
        <Grid container spacing={16}>
            <Grid item md={4} xs={12} style={{marginBottom: 8}}>
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
            </Grid>
            <Grid item md={8} xs={12}>
                <Paper style={{padding: 16}}>
                    <Typography variant="title">
                        Validator declaration
                    </Typography>
                    <Editor
                        value={validatorJSON}
                        onChange={setValidatorJSON}
                        language="json"
                        width="100%"
                        height="40vh"
                        className="dj-code-editor"
                    />
                </Paper>
            </Grid>
        </Grid>
    );
}

export default withStyles(styles, { withTheme: true })(EditQuizTaskPage);
