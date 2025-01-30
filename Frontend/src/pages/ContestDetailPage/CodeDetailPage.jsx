import React, {useEffect, useState} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import VWhitespace from "../../utils/VWhitespace.jsx";
import {getAvailableCompilers, getContest, getContestPage, tryToEnterContest} from "../../api/endpoints-contests.jsx";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import {
    getCodeSolutions,
    getQuizSolutions,
    submitCodeSolution,
    submitQuizSolution
} from "../../api/endpoints-solutions.jsx";
import {
    CircularProgress,
    Grid,
    TextField,
    Typography,
    withStyles,
    Button,
    Paper,
    Table,
    TableHead, TableRow, TableCell, TableBody, FormControl, InputLabel, Select, MenuItem, Icon
} from "@material-ui/core";
import {Editor} from "@monaco-editor/react";
import MarkdownRenderer from "../../components/Markdown/MarkdownRenderer.jsx";
import {lightGreen, teal} from "@material-ui/core/colors";
import {Edit, Visibility} from "@material-ui/icons";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {dateConverter} from "../../utils/time.jsx";
import Preloader from "../../components/Preloader/Preloader.jsx";

const styles = theme => ({
    table: {
        overflowX: "scroll"
    }
});

function CodeDetailPage(props) {
    const {contestId, pageType, pageId} = useParams();
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {contestData, pageData, classes, theme} = props;

    const [solutionText, setSolutionText] = useState(null);
    const [availableCompilers, setAvailableCompilers] = useState(null);
    const [currentHighlightLang, setCurrentHighlightLang] = useState("text");
    const [currentSubmissionLang, setCurrentSubmissionLang] = useState("");
    const [isSubmissionLoading, setIsSubmissionLoading] = useState(false);
    const [previousSolutions, setPreviousSolutions] = useState(null);
    console.log(pageData);
    useEffect(() => {
        getCodeSolutions(accessToken, pageId).then(response => {
            if (response.success) setPreviousSolutions(response.data);
        });
        getAvailableCompilers().then(response => {
            if (response.success) {
                const compilers = {};
                response.data.map(data => {
                    compilers[data[0]] = data[1];
                });
                setAvailableCompilers(compilers);
            }
        })
    }, [pageData]);

    const isFullyLoaded = () => {
        return !(contestData === null || pageData === null || previousSolutions === null
            || availableCompilers === null);
    }

    const onSubmitSolution = () => {
        if (currentSubmissionLang === "" || currentHighlightLang === "text") {
            toastError("Select a compiler first!");
            return;
        }
        setIsSubmissionLoading(true);
        submitCodeSolution(
            accessToken, pageId, solutionText, currentSubmissionLang, "str"
        ).then(response => {
            window.location.href = `/contests/${contestId}/${pageType}/${pageId}`;
            setIsSubmissionLoading(false);
        });
    };

    if (!isFullyLoaded())
        return <Preloader/>;

    return (
        <div>
            <Grid container spacing={24}>
                <Grid item lg={6} xs={12}>
                    <div style={{
                        width: "100%",
                        height: "100%",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "stretch"
                    }}>
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
                        <Paper style={{width: "100%", padding: "1rem", flex: "1 1 auto"}}>
                            <MarkdownRenderer text={pageData.description}/>
                        </Paper>
                    </div>
                </Grid>
                <Grid item lg={6} xs={12}>
                    <Paper style={{width: "100%", padding: "1rem"}}>
                        <Typography variant="headline">
                            Constraints
                        </Typography>
                        <Typography variant="subheading">
                            Time limit: <b>{pageData.test_suite?.time_limit}s</b>
                        </Typography>
                        <Typography variant="subheading">
                            Memory limit: <b>{pageData.test_suite?.mem_limit_mb}MB</b>
                        </Typography>
                    </Paper>
                    <VWhitespace/>
                    <Paper style={{width: "100%", padding: "1rem"}}>
                        <Typography variant="headline">
                            Example test cases
                        </Typography>
                        <Table className={classes.table}>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Input</TableCell>
                                    <TableCell>Output</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>{
                                pageData.test_suite?.public_cases?.map((data, index) => {
                                    return <TableRow>
                                        <TableCell><pre>{data.in}</pre></TableCell>
                                        <TableCell><pre>{data.out}</pre></TableCell>
                                    </TableRow>
                                })
                            }</TableBody>
                        </Table>
                    </Paper>
                </Grid>
            </Grid>
            <Grid container spacing={24}>
                <Grid item lg={6} xs={12}>
                    <Paper style={{width: "100%", padding: "1rem"}}>
                        <Typography variant="headline">Submit code</Typography>
                        <div style={{display: "flex", justifyContent: "space-between", marginTop: 8}}>
                            <FormControl className={classes.formControl}
                                         style={{minWidth: "50%", marginBottom: 8}}>
                                <InputLabel htmlFor="compiler-name">Compiler</InputLabel>
                                <Select
                                    value={currentSubmissionLang}
                                    onChange={e => {
                                        setCurrentSubmissionLang(e.target.value);
                                        setCurrentHighlightLang(availableCompilers[e.target.value]);
                                        console.log(e.target.value, availableCompilers[e.target.value])
                                    }}
                                    inputProps={{
                                        name: 'compiler',
                                        id: 'compiler-name',
                                    }}
                                >{Object.entries(availableCompilers).map((data, index) => {
                                    return <MenuItem key={index} value={data[0]}>{data[0]}</MenuItem>;
                                })}</Select>
                            </FormControl>
                            <Button onClick={onSubmitSolution}
                                disabled={isSubmissionLoading}
                                    variant="raised"
                                style={{margin: 8}}>
                                <Icon>send</Icon><HWhitespace width={0.5}/>Submit
                            </Button>
                        </div>

                        <Editor
                            height="400px" width="100%"
                            language={currentHighlightLang}
                            className="dj-code-editor"
                            onChange={s => setSolutionText(s)}
                            options={{
                                tabSize: 2,
                                fontFamily: "JetBrains Mono"
                            }}
                        />
                    </Paper>
                </Grid>
                <Grid item lg={6} xs={12}>
                    <Paper style={{width: "100%", padding: "1rem"}}>
                        <Typography variant="headline">
                            Your solutions
                        </Typography>
                        <VWhitespace/>
                        <div style={{width: "100%", overflowX: "scroll"}}>
                            <Table className={classes.table} style={{width: "100%"}} padding="dense">
                                <TableHead>
                                    <TableRow>
                                        <TableCell></TableCell>
                                        <TableCell>Verdict</TableCell>
                                        <TableCell>Score</TableCell>
                                        <TableCell>Date</TableCell>
                                        <TableCell>Compiler</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>{previousSolutions.map((data, index) => {
                                    const style = data.short_verdict === "OK"?
                                        {background: lightGreen[300]} : {};
                                    return <TableRow key={index}
                                                     className="table-success"
                                                     style={style} >
                                        <TableCell padding="none" style={{paddingLeft: 8}}>
                                            <Button href={`/solutions/code/${data.id}`} variant="mini">
                                                <Visibility/>
                                            </Button>
                                        </TableCell>
                                        <TableCell>{data.short_verdict}</TableCell>
                                        <TableCell>{data.score}</TableCell>
                                        <TableCell>{dateConverter(data.submitted_at)}</TableCell>
                                        <TableCell>{data.data.compiler}</TableCell>
                                    </TableRow>;
                                })}</TableBody>
                            </Table>
                        </div>
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );

}

export default withStyles(styles, { withTheme: true })(CodeDetailPage);
