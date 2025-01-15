import {Spinner} from "react-bootstrap";
import {CircularProgress, withStyles} from "@material-ui/core";
import React from "react";

const styles = theme => ({});

function Preloader(props) {
    const {theme, classes} = props;
    return <div style={{
        width: "100%",
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    }}><CircularProgress className={classes.progress}/></div>;
}

export default withStyles(styles, { withTheme: true })(Preloader);
