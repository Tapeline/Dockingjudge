import React, {useState} from "react";
import {toastError} from "../../../ui/toasts.jsx";
import {useNavigate} from "react-router-dom";
import {createContest, createTextPage} from "../../../api/endpoints-contests.jsx";
import {Button, Dialog, DialogActions, DialogContent,
    DialogTitle, TextField, withStyles} from "@material-ui/core";
import {Add} from "@material-ui/icons";

const styles = theme => ({});

function DialogImpl(props) {
    const [show, setShow] = useState(false);
    const [pageTitle, setPageTitle] = useState("");
    const [pageDescription, setPageDescription] = useState("");
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [isLoading, setIsLoading] = useState(false);
    const {classes, theme, contestId} = props;

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleSubmit = (e) => {
        e.preventDefault();
        setIsLoading(true);
        createTextPage(accessToken, contestId, {
            name: pageTitle,
            text: pageDescription
        }).then((response) => {
            setIsLoading(false);
            if (!response.success) toastError(response.reason);
            else {
                handleClose();
                window.location.href = window.location.href;
            }
        });
    };

    return (
        <>
            <Button variant="outlined" onClick={handleShow} size="small" style={{width: "100%"}}><Add/> Text</Button>
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
                        onChange={e => setPageTitle(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="desc"
                        multiline
                        label="Page text"
                        type="text"
                        fullWidth
                        onChange={e => setPageDescription(e.target.value)}
                    />
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
