import React, {useState} from "react";
import {toastError} from "../../../ui/toasts.jsx";
import {useNavigate} from "react-router-dom";
import {createContest} from "../../../api/endpoints-contests.jsx";
import {Button, Dialog, DialogActions, DialogContent,
    DialogTitle, TextField, withStyles} from "@material-ui/core";
import {Add} from "@material-ui/icons";

const styles = theme => ({});

function DialogImpl(props) {
    const [show, setShow] = useState(false);
    const [contestName, setContestName] = useState("");
    const [contestDescription, setContestDescription] = useState("");
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [isLoading, setIsLoading] = useState(false);
    const {classes, theme} = props;

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleSubmit = () => {
        setIsLoading(true);
        createContest(accessToken, {
            name: contestName,
            description: contestDescription
        }).then((response) => {
            if (!response.success) toastError(response.reason);
            else {
                handleClose();
                window.location.href = "/contests";
            }
        });
    };

    return (
        <>
            <Button variant="fab" mini onClick={handleShow}><Add/></Button>
            <Dialog
                open={show}
                onClose={handleClose}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Create contest</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Contest name"
                        type="text"
                        fullWidth
                        onChange={e => setContestName(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="desc"
                        label="Short description"
                        type="text"
                        fullWidth
                        onChange={e => setContestDescription(e.target.value)}
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
