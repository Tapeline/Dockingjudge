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

    useEffect(() => {
        getContest(accessToken, contestId).then(response => {
            if (response.success) {
                setContestData(response.data);
                if (pageType === null || pageType === undefined) {
                    window.location.href = "/contests/" + contestId +
                        "/" + response.data.pages[0].type + "/" + response.data.pages[0].id;
                }
            } else setContestNotFound(true);
        });
    }, []);

    useEffect(() => {
        if (pageType === null || pageType === undefined) return;
        getContestPage(accessToken, contestId, pageType, pageId).then(response => {
            if (response.success)
                setPageData(response.data);
        })
    }, [pageType, pageId]);

    const isFullyLoaded = () => {
        return !(contestData === null || pageData === null);
    }

    const onEnterClick = () => {
        tryToEnterContest(accessToken, contestId).then(response => {
            if (response.success) {
                toastSuccess("Successfully entered contest");
                window.location.href = `/contests/${contestId}/${pageType}/${pageId}`;
            } else toastError(response.errorCode);
        })
    }

    if (isContestNotFound)
        return <h1>Contest not found</h1>;

    if (!isFullyLoaded())
        return <CircularProgress className={classes.progress}/>;

    if (pageType === "text") {
        return (
            <div>
                <Typography variant="display2">
                    {pageData.name}
                    {
                        contestData.author === localStorage.getItem("accountId")
                            ? <Button mini style={{marginLeft: 16}}
                                href={`/contests/${contestId}/${pageType}/${pageId}/edit`}
                            ><Edit/></Button>
                            : ""
                    }
                </Typography>
                <Typography variant="body1">{pageData.text}</Typography>
                {pageData?.is_enter_page
                    ? <Button onClick={onEnterClick}>Enter contest</Button>
                    : ""}
            </div>
        );
    } else if (pageType === "quiz") {
        return <QuizDetailPage contestData={contestData} pageData={pageData}/>;
    } else if (pageType === "code") {
        return <CodeDetailPage contestData={contestData} pageData={pageData}/>;
    }

}

export default withStyles(styles, { withTheme: true })(ContestDetailPage);
