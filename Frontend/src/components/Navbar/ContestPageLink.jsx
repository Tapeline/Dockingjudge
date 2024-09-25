import {NavLink, useNavigate} from "react-router-dom";
import React from "react";
import {ListItem, ListItemIcon, ListItemText} from "@material-ui/core";
import {Code, Description, Edit, Inbox} from "@material-ui/icons";

export default function ContestPageLink(props) {
    const {contestId, data, closeCallback} = props;
    const navigate = useNavigate();

    const title = data.type === "text"? data.content.name : data.content.title;

    let icon;
    if (data.type === "text")
        icon = (<Description/>);
    else if (data.type === "quiz")
        icon = (<Edit/>);
    else if (data.type === "code")
        icon = (<Code/>);

    return (
        <ListItem button key={data.id}
                  onClick={() => {
                      navigate(`/contests/${contestId}/${data.type}/${data.id}`);
                      setTimeout(closeCallback, 100);
                  }}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText primary={title}/>
        </ListItem>
    );
}
