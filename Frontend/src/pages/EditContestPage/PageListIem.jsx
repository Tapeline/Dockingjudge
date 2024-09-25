import React from "react";
import {IconButton, ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText, withStyles} from "@material-ui/core";
import {Code, Delete, Description, Edit} from "@material-ui/icons";
import {deleteCodePage, deleteQuizPage, deleteTextPage} from "../../api/endpoints-contests.jsx";
import {toastError} from "../../ui/toasts.jsx";
import {useNavigate} from "react-router-dom";

const styles = theme => ({});

function PageListItem(props) {
    const {classes, theme, contestId, data} = props;

    const title = data.type === "text"? data.content.name : data.content.title;
    const navigate = useNavigate();

    let icon;
    if (data.type === "text")
        icon = (<Description/>);
    else if (data.type === "quiz")
        icon = (<Edit/>);
    else if (data.type === "code")
        icon = (<Code/>);

    const handleDeletePage = () => {
        let delFunc;
        if (data.type === "text") delFunc = deleteTextPage;
        else if (data.type === "quiz") delFunc = deleteQuizPage;
        else if (data.type === "code") delFunc = deleteCodePage;
        delFunc(localStorage.getItem("accessToken"), contestId, data.id).then(response => {
            if (response.success)
                window.location.href = window.location.href;
            else
                toastError(response.reason);
        });
    }

    return (<>
        <ListItem button onClick={() => navigate(`/contests/${contestId}/${data.type}/${data.id}/edit`)}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText primary={title}/>
            <ListItemSecondaryAction>
                <IconButton aria-label="Delete" onClick={handleDeletePage}>
                    <Delete/>
                </IconButton>
            </ListItemSecondaryAction>
        </ListItem>
    </>)
}

export default withStyles(styles, { withTheme: true })(PageListItem);
