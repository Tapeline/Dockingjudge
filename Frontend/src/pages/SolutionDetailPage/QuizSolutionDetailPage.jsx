import React, {isValidElement, useEffect, useState} from "react";
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
import Preloader from "../../components/Preloader/Preloader.jsx";
import {amber, deepOrange, lightGreen, lime, orange} from "@material-ui/core/colors";
import VWhitespace from "../../utils/VWhitespace.jsx";
import {getScoreColor} from "../../utils/scoreColors.jsx";

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
        return <Preloader/>;

    return (<>
        <div style={{width: "100%", display: "flex", flexDirection: "column", alignItems: "center"}}>
            <div className="dj-under-card-bg" style={{background: getScoreColor(solutionData.points)}}></div>
            <Paper className="dj-solution-paper">
                <Typography variant="headline">
                    Quiz solution {solutionId}
                </Typography>
                <VWhitespace/>
                <Typography variant="subheading" style={{display: "flex", alignItems: "center"}}>
                    <Stars/>
                    <HWhitespace width={1}/>
                    Score: <HWhitespace width={0.5}/>
                    <code>{solutionData.points}</code>
                    <HWhitespace width={1}/>
                    {solutionData.is_solved? <Check/> : <Close/>}
                </Typography>
                <Typography variant="caption" style={{display: "flex", alignItems: "center"}}>
                    <Timer/>
                    <HWhitespace width={1}/>
                    Submitted at: <HWhitespace width={0.5}/>
                    {dateConverter(solutionData.submitted_at)}
                </Typography>
                <VWhitespace/>
                <Typography variant="headline">
                    Your answer
                </Typography>
                <pre>{solutionData.text}</pre>
            </Paper>
        </div>
    </>);
}

export default withStyles(styles, { withTheme: true })(QuizSolutionDetailPage);
