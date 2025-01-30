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
import {getCodeFile, getCodeSolution} from "../../api/endpoints-solutions.jsx";
import {dateConverter} from "../../utils/time.jsx";
import {Check, Close, Code, Info, Stars, Timer} from "@material-ui/icons";
import HWhitespace from "../../utils/HWhitespace.jsx";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getScoreColor} from "../../utils/scoreColors.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";
import SyntaxHighlighter from "react-syntax-highlighter";

const styles = theme => ({
    paper: {
        marginTop: 8,
        marginBottom: 8,
        padding: 16
    }
});

function CodeSolutionDetailPage(props) {
    const {solutionId} = useParams();
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {theme, classes} = props;
    const [isNotFound, setNotFound] = useState(false);
    const [solutionData, setSolutionData] = useState(null);
    const [solutionText, setSolutionText] = useState(null);

    useEffect(() => {
        getCodeSolution(accessToken, solutionId).then(response => {
            if (response.success) {
                setSolutionData(response.data);
                getCodeFile(response.data.data.submission_url).then(r => {
                    setSolutionText(r.data);
                })
            } else setNotFound(true);
        });
    }, []);

    const isFullyLoaded = () => {
        return !(solutionData === null || solutionText === null);
    }

    if (isNotFound)
        return <h1>Solution not found</h1>;

    if (!isFullyLoaded())
        return <Preloader/>;

    return (<>
        <div style={{width: "100%", display: "flex", flexDirection: "column", alignItems: "center"}}>
            <div className="dj-under-card-bg" style={{background: getScoreColor(solutionData.score)}}></div>
            <Paper className="dj-solution-paper">
                <Typography variant="headline">
                    Code solution {solutionId}
                </Typography>
                <VWhitespace/>
                <Typography variant="subheading" style={{display: "flex", alignItems: "center"}}>
                    <Stars/>
                    <HWhitespace width={1}/>
                    Score: <HWhitespace width={0.5}/>
                    <code>{solutionData.score}</code>
                    <HWhitespace width={1}/>
                    {solutionData.short_verdict === "OK" ? <Check/> : <Close/>}
                </Typography>
                <Typography variant="caption" style={{display: "flex", alignItems: "center"}}>
                    <Timer/>
                    <HWhitespace width={1}/>
                    Submitted at: <HWhitespace width={0.5}/>
                    {dateConverter(solutionData.submitted_at)}
                </Typography>
                <Typography variant="caption" style={{display: "flex", alignItems: "center"}}>
                    <Code/>
                    <HWhitespace width={1}/>
                    Compiler: <HWhitespace width={0.5}/>
                    {solutionData.data.compiler}
                </Typography>
                <VWhitespace/>
                <Typography variant="body1" style={{display: "flex", alignItems: "start"}}>
                    <Info/>
                    <HWhitespace width={1}/>
                    <pre style={{margin: 0}}>{solutionData.data.detailed_verdict}</pre>
                </Typography>
                <VWhitespace/>
                <Typography variant="headline">
                    Group scores
                </Typography>
                <Table className={classes.table}>
                    <TableHead>
                        <TableRow>
                            <TableCell>Group</TableCell>
                            <TableCell>Score</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>{
                        Object.entries(solutionData.data.group_scores).map(
                            (data, index) => {
                                return <TableRow key={index}>
                                    <TableCell>{data[0]}</TableCell>
                                    <TableCell>{data[1]}</TableCell>
                                </TableRow>;
                            })
                    }</TableBody>
                </Table>
                <VWhitespace/>
                <Typography variant="headline">
                    Your answer
                </Typography>
                <div className="rendered-md">
                    <SyntaxHighlighter
                        customStyle={{padding: "1rem", background: null}}
                        language={solutionData.compiler}
                    >{solutionText}</SyntaxHighlighter>
                </div>
            </Paper>
        </div>
    </>
);
}

export default withStyles(styles, { withTheme: true })(CodeSolutionDetailPage);
