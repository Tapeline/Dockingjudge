import React, {useEffect, useState} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import VWhitespace from "../../utils/VWhitespace.jsx";
import {getContest, getContestPage, tryToEnterContest} from "../../api/endpoints-contests.jsx";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import {getQuizSolutions, submitQuizSolution} from "../../api/endpoints-solutions.jsx";
import {
    CircularProgress,
    Grid,
    TextField,
    Typography,
    withStyles,
    Button,
    Paper,
    Table,
    TableHead, TableRow, TableCell, TableBody, Icon
} from "@material-ui/core";
import {lightGreen} from "@material-ui/core/colors";
import MarkdownRenderer from "../../components/Markdown/MarkdownRenderer.jsx";
import {Edit} from "@material-ui/icons";
import HWhitespace from "../../utils/HWhitespace.jsx";
import Preloader from "../../components/Preloader/Preloader.jsx";

const styles = theme => ({});

function QuizDetailPage(props) {
    const {contestId, pageType, pageId} = useParams();
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {contestData, pageData, classes, theme} = props;

    const [solutionText, setSolutionText] = useState(null);
    const [isSubmissionLoading, setIsSubmissionLoading] = useState(false);
    const [previousSolutions, setPreviousSolutions] = useState(null);

    console.log(pageData);
    useEffect(() => {
        getQuizSolutions(accessToken, pageId).then(response => {
            if (response.success) setPreviousSolutions(response.data);
        });
    }, []);

    const isFullyLoaded = () => {
        return !(contestData === null || pageData === null || previousSolutions === null);
    }

    const onSubmitSolution = () => {
        setIsSubmissionLoading(true);
        submitQuizSolution(accessToken, pageId, solutionText).then(response => {
            window.location.href = `/contests/${contestId}/${pageType}/${pageId}`;
            setIsSubmissionLoading(false);
        });
    };

    if (!isFullyLoaded())
        return <Preloader/>;

    return (
        <div>
            <Typography variant="display2">
                {pageData.title}
                {
                    contestData.author == localStorage.getItem("accountId")
                        ? <Button mini style={{marginLeft: 16}}
                            href={`/contests/${contestId}/${pageType}/${pageId}/edit`}
                        ><Edit/></Button>
                        : ""
                }
            </Typography>
            <VWhitespace/>
            <Paper style={{width: "100%", padding: "1rem"}}>
                <div style={{maxWidth: 1200}}>
                    <MarkdownRenderer text={pageData.description}/>
                </div>
            </Paper>
            <VWhitespace/>
            <Grid container spacing={24}>
                <Grid item md={8} xs={12} style={{display: "flex"}}>
                    <Paper style={{width: "100%", padding: "1rem"}}>
                        <Typography variant="headline">Submit answer</Typography>
                        <TextField
                            autoFocus
                            margin="dense"
                            id="name"
                            label="Answer"
                            type="text"
                            fullWidth
                            multiline
                            onChange={e => setSolutionText(e.target.value)}
                        />
                        <div>
                            <Button onClick={onSubmitSolution}
                                disabled={isSubmissionLoading}
                                    variant="raised"
                                style={{margin: 8}}>
                            <Icon>send</Icon><HWhitespace width={0.5}/>Submit
                        </Button>
                        </div>
                    </Paper>
                </Grid>
                <Grid item md={4} xs={12}>
                    <Paper style={{height: "100%", width: "100%", padding: "1rem"}}>
                        <Typography variant="headline">
                            Your solutions
                        </Typography>
                        <Table className={classes.table}>
                            <TableHead>
                                <TableRow>
                                    <TableCell>#</TableCell>
                                    <TableCell>Score</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>{previousSolutions.map((data, index) => {
                                const style = data.is_solved? {background: lightGreen[300]} : {};
                                return <TableRow key={index} className="table-success" style={style}>
                                    <TableCell>
                                        <Button href={`/solutions/quiz/${data.id}`}>{data.id}</Button>
                                    </TableCell>
                                    <TableCell>{data.points}</TableCell>
                                </TableRow>;
                            })}</TableBody>
                        </Table>
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );

}

export default withStyles(styles, { withTheme: true })(QuizDetailPage);
