import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {
    getAllContests,
    getContest,
    getContestPage, modifyContest,
    modifyQuizPage,
    modifyTextPage
} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {
    Button,
    CircularProgress, FormControl,
    FormControlLabel, FormHelperText,
    Grid, Input, InputAdornment, List,
    Paper, Switch,
    TextField, Toolbar,
    Typography, Tab, Tabs,
    withStyles, AppBar
} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";
import {Editor} from "@monaco-editor/react";
import {Save} from "@material-ui/icons";
import {lightGreen} from "@material-ui/core/colors";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";
import PageListItem from "./PageListIem.jsx";
import CreateTextPageDialog from "../../components/Dialogs/CreatePageDialog/CreateTextPageDialog.jsx";
import CreateCodePageDialog from "../../components/Dialogs/CreatePageDialog/CreateCodePageDialog.jsx";
import CreateQuizPageDialog from "../../components/Dialogs/CreatePageDialog/CreateQuizPageDialog.jsx";

const styles = theme => ({});

function EditContestPage(props) {
    const navigate = useNavigate();
    const {contestId} = useParams();
    const accessToken = localStorage.getItem("accessToken");
    const [contestData, setContestData] = useState(null);
    const {classes, theme} = props;

    const [contestTitle, setContestTitle] = useState(null);
    const [contestDescription, setContestDescription] = useState(null);
    const [pagesJSON, setPagesJSON] = useState(null);
    const [isStarted, setIsStarted] = useState(null);
    const [isEnded, setIsEnded] = useState(null);
    const [timeLimit, setTimeLimit] = useState(null);
    const [tabValue, setTabValue] = useState(0);

    useEffect(() => {
        getContest(accessToken, contestId).then(response => {
            setContestData(response.data);
            setContestTitle(response.data.name);
            setContestDescription(response.data.description);
            setIsStarted(response.data.is_started);
            setIsEnded(response.data.is_ended);
            setTimeLimit(response.data.time_limit_seconds);
            let pages = [];
            response.data.pages.forEach(page => {
                pages.push({type: page.type, id: page.id});
            })
            setPagesJSON(JSON.stringify(pages, null, 2));
        });
    }, []);

    const applyChanges = () => {
        let pagesParsed;
        try {
            pagesParsed = JSON.parse(pagesJSON);
        } catch (err) {
            toastError(err.toString());
            return;
        }
        modifyContest(accessToken, contestId, {
            name: contestTitle,
            description: contestDescription,
            is_started: isStarted,
            pages: pagesParsed
        }).then(response => {
            if (!response.success) {
                toastError(response.reason);
                return;
            }
            toastSuccess("Saved");
        })
    };

    return (
        contestData === null || contestTitle === null || contestDescription === null ||
            timeLimit === null || isEnded === null || isStarted === null?
        <CircularProgress className={classes.progress}/>
        :
            <div>
                <Typography variant="display2">
                    Contest settings
                </Typography>
                <VWhitespace/>
                <Button onClick={applyChanges} mini fullWidth
                        style={{marginBottom: 8}}
                        variant="raised">
                    <Save/>&nbsp;Save
                </Button>
                <VWhitespace/>
                <Typography variant="title">
                    General
                </Typography>
                <TextField
                    id="title"
                    label="Title"
                    value={contestTitle}
                    onChange={e => setContestTitle(e.target.value)}
                    margin="normal"
                    fullWidth
                />
                <br/>
                <TextField
                    id="desc"
                    label="Description"
                    multiline
                    value={contestDescription}
                    onChange={e => setContestDescription(e.target.value)}
                    margin="normal"
                    fullWidth
                />
                <br/>
                <FormControlLabel
                    control={
                        <Switch
                            checked={isStarted}
                            onChange={e => setIsStarted(e.target.checked)}
                        />
                    }
                    label="Is started?"
                />
                <HWhitespace/>
                <FormControlLabel
                    control={
                        <Switch
                            checked={isEnded}
                            onChange={e => setIsEnded(e.target.checked)}
                        />
                    }
                    label="Is ended?"
                />
                <HWhitespace/>
                <FormControl aria-describedby="time-limit-helper-text">
                    <Input
                        id="time-limit"
                        value={timeLimit}
                        onChange={e => {
                            if (e.target.value < 0)
                                setTimeLimit(-1)
                            else
                                setTimeLimit(e.target.value)
                        }}
                        endAdornment={<InputAdornment position="end">seconds</InputAdornment>}
                        inputProps={{
                            'aria-label': 'Time limit',
                        }}
                        type="number"
                    />
                    <FormHelperText id="time-limit-helper-text">Time limit</FormHelperText>
                </FormControl>
                <VWhitespace/>
                <Typography variant="title">
                    Pages
                </Typography>
                <VWhitespace/>
                <div>
                    <AppBar position="static">
                        <Tabs value={tabValue} onChange={(event, value) => {
                            setTabValue(value);
                        }}>
                            <Tab label="Page list"/>
                            <Tab label="JSON"/>
                        </Tabs>
                    </AppBar>
                    {tabValue === 0 && <>
                        <VWhitespace/>
                        <Toolbar variant="dense"
                                 indicatorColor="primary"
                                 textColor="primary"
                        >
                            <Grid container spacing={24}>
                                <Grid item xs={4} sm={2}>
                                    <CreateTextPageDialog contestId={contestId}/>
                                </Grid>
                                <Grid item xs={4} sm={2}>
                                    <CreateQuizPageDialog contestId={contestId}/>
                                </Grid>
                                <Grid item xs={4} sm={2}>
                                    <CreateCodePageDialog contestId={contestId}/>
                                </Grid>
                            </Grid>
                        </Toolbar>
                        <List>{
                            contestData.pages.map((data, index) => {
                                return <PageListItem contestId={contestId} data={data}/>;
                            })
                        }</List>
                    </>}
                    {tabValue === 1 && <>
                        <Editor
                            value={pagesJSON}
                            onChange={setPagesJSON}
                            language="json"
                            width="100%"
                            height="80vh"
                            options={{
                                tabSize: 2,
                                fontFamily: "JetBrains Mono"
                            }}
                        />
                    </>}
                </div>
            </div>
    );
}

export default withStyles(styles, {withTheme: true})(EditContestPage);
