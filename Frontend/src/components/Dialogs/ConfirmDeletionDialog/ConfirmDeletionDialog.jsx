import React, {useState} from "react";
import {toastError} from "../../../ui/toasts.jsx";
import {useNavigate} from "react-router-dom";
import {createContest} from "../../../api/endpoints-contests.jsx";
import {
    Button, Dialog, DialogActions, DialogContent,
    DialogTitle, TextField, Typography, withStyles
} from "@material-ui/core";
import {Add, Delete} from "@material-ui/icons";
import {red} from "@material-ui/core/colors";

const styles = theme => ({});

function DialogImpl(props) {
    const [show, setShow] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const {classes, theme, onOk, onCancel, buttonText, header, text} = props;

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleSubmit = (e) => {
        e.preventDefault();
        setIsLoading(true);
        onOk();
    };

    return (
        <>
            <Button onClick={handleShow}
                    variant="outlined" style={{color: red[500], borderColor: red[500]}}>
                <Delete/> {buttonText}</Button>
            <Dialog
                open={show}
                onClose={handleClose}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">{header}</DialogTitle>
                <DialogContent>
                    <Typography>{text}</Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} style={{color: red[500], borderColor: red[500]}} disabled={isLoading}>
                        <Delete/> Delete
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default withStyles(styles, { withTheme: true })(DialogImpl);

