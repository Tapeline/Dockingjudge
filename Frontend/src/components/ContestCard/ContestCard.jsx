import React from "react";
import {Link} from "react-router-dom";
import {Button, Card, CardActions, CardContent, Typography, withStyles} from "@material-ui/core";

const styles = theme => ({
    card: {
        marginBottom: 8
    }
});

function ContestCard(props) {
    const {data, classes, theme} = props;

    return (
        <Card className={classes.card}>
            <CardContent>
                <Typography gutterBottom variant="headline" component="h2">
                    {data.name}
                </Typography>
                <Typography component="p">
                    {data.description}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="small" color="primary" href={"/contests/" + data.id}>
                    Open
                </Button>
            </CardActions>
        </Card>
    )
}

export default withStyles(styles, { withTheme: true })(ContestCard);
