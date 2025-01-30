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
import {Spinner} from "react-bootstrap";
import VWhitespace from "../../utils/VWhitespace.jsx";

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
    const [quizScore, setQuizScore] = useState("0");

    useEffect(() => {
        getContestPage(accessToken, contestId, "quiz", pageId).then(response => {
            setPageData(response.data);
            setPageTitle(response.data.title);
            setPageDescription(response.data.description);
            setQuizScore(response.data.points);
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
            validator: validatorParsed,
            points: parseInt(quizScore)
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
        <Preloader/>
        :
        <Grid container spacing={16}>
            <Grid item md={4} xs={12}>
                <Paper style={{width: "100%", height: "100%", padding: "1rem"}}>
                    <Typography variant="headline">
                        Edit quiz task
                    </Typography>
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
                        required
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
                        required
                    />
                    <br/>
                    <TextField
                        margin="dense"
                        id="score"
                        label="Question points"
                        type="number"
                        fullWidth
                        required
                        value={quizScore}
                        onChange={e => setQuizScore(e.target.value)}
                    />
                </Paper>

            </Grid>
            <Grid item md={8} xs={12}>
                <Paper style={{padding: 16}}>
                    <Typography variant="headline">
                        Validator declaration
                    </Typography>
                    <VWhitespace/>
                    <Editor
                        value={validatorJSON}
                        onChange={setValidatorJSON}
                        language="json"
                        width="100%"
                        height="40vh"
                        options={{
                            tabSize: 2,
                            fontFamily: "JetBrains Mono"
                        }}
                    />
                </Paper>
            </Grid>
        </Grid>
    );
}

export default withStyles(styles, { withTheme: true })(EditQuizTaskPage);
