import React, {useEffect, useState} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import {
    CircularProgress,
    Typography,
    withStyles,
    Button,
    Paper,
    TableHead,
    TableRow,
    TableCell, TableBody, Table, Grid
} from "@material-ui/core";
import {getCodeSolution, getQuizSolution} from "../../api/endpoints-solutions.jsx";
import {dateConverter} from "../../utils/time.jsx";
import {Check, Close, Code, Stars, Timer} from "@material-ui/icons";
import HWhitespace from "../../utils/HWhitespace.jsx";

const styles = theme => ({
    paper: {
        marginTop: 8,
        marginBottom: 8,
        padding: 16
    }
});

function QuizSolutionDetailPage(props) {
    const {solutionId} = useParams();
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {theme, classes} = props;
    const [isNotFound, setNotFound] = useState(false);
    const [solutionData, setSolutionData] = useState(null);

    useEffect(() => {
        getQuizSolution(accessToken, solutionId).then(response => {
            if (response.success) {
                setSolutionData(response.data);
            } else setNotFound(true);
        });
    }, []);

    const isFullyLoaded = () => {
        return !(solutionData === null);
    }

    if (isNotFound)
        return <h1>Solution not found</h1>;

    if (!isFullyLoaded())
        return <CircularProgress className={classes.progress}/>;

    return (<>
        <Grid container spacing={16}>
            <Grid item md={3} xs={12}>
                <Typography variant="display2">
                    Solution #quiz/{solutionId}
                </Typography>
                <Typography variant="display1">
                    <Stars/> Score: <code>{solutionData.points}</code>
                    <HWhitespace width={1}/>
                    {solutionData.is_solved? <Check/> : <Close/>}
                </Typography>
                <Typography variant="caption" styles={{verticalAlign: 'center'}}>
                    <Timer/> Submitted at: {dateConverter(solutionData.submitted_at)}
                </Typography>
            </Grid>
            <Grid item md={9} xs={12}>
                <Paper className={classes.paper}>
                    <Typography variant="headline">
                        Your answer
                    </Typography>
                    <pre>{solutionData.text}</pre>
                </Paper>
            </Grid>
        </Grid>


    </>);

}

export default withStyles(styles, { withTheme: true })(QuizSolutionDetailPage);
