import React, {useState} from "react";
import {Button, Modal} from "react-bootstrap";
import {useNavigate} from "react-router-dom";

export default function ConfirmDeletionDialog(props) {
    const [show, setShow] = useState(false);
    const {onOk, onCancel, buttonText, header, text} = props;

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleSubmit = (e) => {
        e.preventDefault();
        onOk();
    };

    return (
        <>
            <Button variant="outline-danger" onClick={handleShow}>
                <i className="bi bi-trash"></i> {buttonText}
            </Button>

            <Modal show={show} onHide={handleClose} className="alert-danger">
                <Modal.Header closeButton>
                    <Modal.Title>{header}?</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {text}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="outline-danger" type="submit" onClick={handleSubmit}>
                        Yes, proceed</Button>
                    <Button variant="secondary" type="submit" onClick={handleClose}>
                        No, cancel</Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}
