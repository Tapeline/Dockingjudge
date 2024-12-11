import React, {useState} from "react";
import {toastError} from "../../../ui/toasts.jsx";
import {useNavigate} from "react-router-dom";
import {createContest, createQuizPage, createTextPage} from "../../../api/endpoints-contests.jsx";
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
    const [quizScore, setQuizScore] = useState("0");
    const [validatorJSON, setValidatorJSON] = useState(
        "{\n" +
        '  "type": "",\n' +
        '  "pattern": ""\n' +
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
            validatorParsed = JSON.parse(validatorJSON);
        } catch (err) {
            toastError(err.toString());
            return;
        }
        setIsLoading(true);
        createQuizPage(accessToken, contestId, {
            title: pageTitle,
            description: pageDescription,
            validator: validatorParsed,
            points: parseInt(quizScore)
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
            <Button variant="outlined" onClick={handleShow} size="small"  style={{width: "100%"}}><Add/> Quiz</Button>
            <Dialog
                open={show}
                onClose={handleClose}
                aria-labelledby="form-dialog-title"
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
                        required
                        onChange={e => setPageTitle(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="desc"
                        label="Page text"
                        type="text"
                        fullWidth
                        required
                        onChange={e => setPageDescription(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="score"
                        label="Question points"
                        type="text"
                        fullWidth
                        required
                        onChange={e => setQuizScore(e.target.value)}
                    />
                    <VWhitespace/>
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
