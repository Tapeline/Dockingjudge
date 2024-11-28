import {useEffect, useState} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import VWhitespace from "../../utils/VWhitespace.jsx";
import {getContest, getContestPage, tryToEnterContest} from "../../api/endpoints-contests.jsx";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import QuizDetailPage from "./QuizDetailPage.jsx";
import {CircularProgress, Typography, withStyles, Button} from "@material-ui/core";
import CodeDetailPage from "./CodeDetailPage.jsx";
import {Edit} from "@material-ui/icons";

const styles = theme => ({});

function ContestDetailPage(props) {
    const {contestId, pageType, pageId} = useParams();
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {theme, classes} = props;
    const [isContestNotFound, setContestNotFound] = useState(false);
    const [contestData, setContestData] = useState(null);
    const [pageData, setPageData] = useState(null);
    const [receivedPageType, setReceivedPageType] = useState(pageType);
    const [receivedPageId, setReceivedPageId] = useState(pageId);

    useEffect(() => {
        getContest(accessToken, contestId).then(response => {
            if (response.success) {
                setContestData(response.data);
                if (receivedPageType === null || receivedPageType === undefined) {
                    setReceivedPageType(response.data.pages[0].type);
                    setReceivedPageId(response.data.pages[0].id);
                }
            } else setContestNotFound(true);
        });
    }, []);

    useEffect(() => {
        if (receivedPageType === null || receivedPageType === undefined) return;
        if (pageType !== undefined) {
            setReceivedPageType(pageType);
            setReceivedPageId(pageId);
        }
        getContestPage(accessToken, contestId, receivedPageType, receivedPageId).then(response => {
            if (response.success)
                setPageData(response.data);
        })
    }, [receivedPageType, receivedPageId, pageType, pageId]);

    const isFullyLoaded = () => {
        return !(contestData === null || pageData === null);
    }

    const onEnterClick = () => {
        tryToEnterContest(accessToken, contestId).then(response => {
            if (response.success) {
                toastSuccess("Successfully entered contest");
                window.location.href = `/contests/${contestId}/${pageType}/${pageId}`;
            } else toastError(response.reason);
        })
    }

    if (isContestNotFound)
        return <h1>Contest not found</h1>;

    if (!isFullyLoaded())
        return <CircularProgress className={classes.progress}/>;

    if (receivedPageType === "text") {
        return (
            <div>
                <Typography variant="display2">
                    {pageData.name}
                    {
                        contestData.author === localStorage.getItem("accountId")
                            ? <Button mini style={{marginLeft: 16}}
                                href={`/contests/${contestId}/${receivedPageType}/${receivedPageId}/edit`}
                            ><Edit/></Button>
                            : ""
                    }
                </Typography>
                <VWhitespace/>
                <Typography variant="body1">{pageData.text}</Typography>
                <VWhitespace/>
                {pageData?.is_enter_page
                    ? <Button variant="outlined" onClick={onEnterClick}>Enter contest</Button>
                    : ""}
            </div>
        );
    } else if (receivedPageType === "quiz") {
        return <QuizDetailPage contestData={contestData} pageData={pageData}/>;
    } else if (receivedPageType === "code") {
        return <CodeDetailPage contestData={contestData} pageData={pageData}/>;
    }

}

export default withStyles(styles, { withTheme: true })(ContestDetailPage);
