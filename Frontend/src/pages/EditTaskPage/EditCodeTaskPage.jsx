import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests, getContestPage, modifyCodePage, modifyQuizPage} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {Button, CircularProgress, Grid, Paper, TextField, Typography, withStyles} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {Editor} from "@monaco-editor/react";
import {Save} from "@material-ui/icons";
import {lightGreen} from "@material-ui/core/colors";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";

const styles = theme => ({});

function EditCodeTaskPage(props) {
    const navigate = useNavigate();
    const {contestId, pageId} = useParams();
    const accessToken = localStorage.getItem("accessToken");
    const [pageData, setPageData] = useState(null);
    const {classes, theme} = props;

    const [pageTitle, setPageTitle] = useState(null);
    const [pageDescription, setPageDescription] = useState(null);
    const [testSuiteJSON, setTestSuiteJSON] = useState(null);

    useEffect(() => {
        getContestPage(accessToken, contestId, "code", pageId).then(response => {
            setPageData(response.data);
            setPageTitle(response.data.title);
            setPageDescription(response.data.description);
            setTestSuiteJSON(JSON.stringify(response.data.test_suite, null, 2));
        });
    }, []);

    const applyChanges = () => {
        let jsonParsed;
        try {
            jsonParsed = JSON.parse(testSuiteJSON);
        } catch (err) {
            toastError(err.toString());
            return;
        }
        modifyCodePage(accessToken, contestId, pageId, {
            title: pageTitle,
            description: pageDescription,
            test_suite: jsonParsed
        }).then(response => {
            if (!response.success) {
                toastError(response.reason);
                return;
            }
            toastSuccess("Saved");
        })
    };

    return (
        pageData === null || testSuiteJSON === null?
        <Preloader/>
        :
        <Grid container spacing={16} style={{height: "100%"}}>
            <Grid item md={4} xs={12}>
                <Paper style={{width: "100%", height: "100%", padding: "1rem"}}>
                    <Typography variant="headline">Edit code task</Typography>
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
                </Paper>
            </Grid>
            <Grid item md={8} xs={12}>
                <Paper style={{padding: 16, height: "100%"}}>
                    <Typography variant="headline">
                        Test suite declaration
                    </Typography>
                    <Editor
                        value={testSuiteJSON}
                        onChange={setTestSuiteJSON}
                        language="json"
                        width="100%"
                        height="80vh"
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

export default withStyles(styles, { withTheme: true })(EditCodeTaskPage);
