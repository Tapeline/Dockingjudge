import React, {useState} from "react";
import {toastError} from "../../../ui/toasts.jsx";
import {useNavigate} from "react-router-dom";
import {createCodePage, createContest, createQuizPage, createTextPage} from "../../../api/endpoints-contests.jsx";
import {
    Button, Dialog, DialogActions, DialogContent,
    DialogTitle, Paper, TextField, Typography, withStyles
} from "@material-ui/core";
import {Add} from "@material-ui/icons";
import {Editor} from "@monaco-editor/react";
import VWhitespace from "../../../utils/VWhitespace.jsx";

const styles = theme => ({});

function DialogImpl(props) {
    const [show, setShow] = useState(false);
    const [pageTitle, setPageTitle] = useState("");
    const [pageDescription, setPageDescription] = useState("");
    const [testSuiteJSON, setTestSuiteJSON] = useState(
        "{\n" +
        '  "groups": [],\n' +
        '  "precompile": [],\n' +
        '  "time_limit": 1,\n' +
        '  "mem_limit_mb": 256,\n' +
        '  "public_cases": []\n' +
        '}'
    );
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [isLoading, setIsLoading] = useState(false);
    const {classes, theme, contestId} = props;

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleSubmit = (e) => {
        e.preventDefault();
        let validatorParsed;
        try {
            validatorParsed = JSON.parse(testSuiteJSON);
        } catch (err) {
            toastError(err.toString());
            return;
        }
        setIsLoading(true);
        createCodePage(accessToken, contestId, {
            title: pageTitle,
            description: pageDescription,
            test_suite: validatorParsed
        }).then((response) => {
            if (!response.success) toastError(response.reason);
            else {
                handleClose();
                window.location.href = window.location.href;
            }
        });
    };

    return (
        <>
            <Button variant="outlined" onClick={handleShow} style={{width: "100%"}}><Add/> Code</Button>
            <Dialog
                open={show}
                onClose={handleClose}
                aria-labelledby="form-dialog-title"
                fullWidth
            >
                <DialogTitle id="form-dialog-title">Create page</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Title"
                        type="text"
                        fullWidth
                        onChange={e => setPageTitle(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="desc"
                        label="Page text"
                        multiline
                        type="text"
                        fullWidth
                        onChange={e => setPageDescription(e.target.value)}
                    />
                    <VWhitespace/>
                    <Paper style={{padding: 16}}>
                        <Typography variant="title">
                            Test suite declaration
                        </Typography>
                        <Editor
                            value={testSuiteJSON}
                            onChange={setTestSuiteJSON}
                            language="json"
                            width="100%"
                            height="40vh"
                            options={{
                                tabSize: 2,
                                fontFamily: "JetBrains Mono"
                            }}
                        />
                    </Paper>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} color="primary" disabled={isLoading}>
                        Create
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default withStyles(styles, { withTheme: true })(DialogImpl);
