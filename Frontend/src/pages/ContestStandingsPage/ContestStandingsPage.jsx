import React, {useEffect, useState} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import VWhitespace from "../../utils/VWhitespace.jsx";
import {getContest} from "../../api/endpoints-contests.jsx";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import {
    CircularProgress,
    Typography,
    withStyles,
    Button,
    Paper,
    Table,
    TableHead,
    TableRow,
    TableCell, TableBody
} from "@material-ui/core";
import {Edit} from "@material-ui/icons";
import {getStandings} from "../../api/endpoints-solutions.jsx";
import {amber, lightGreen} from "@material-ui/core/colors";
import Preloader from "../../components/Preloader/Preloader.jsx";

const styles = theme => ({
    paper: {
        overflowX: "scroll"
    }
});

function ContestStandingsPage(props) {
    const {contestId, pageType, pageId} = useParams();
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const {theme, classes} = props;
    const [isContestNotFound, setContestNotFound] = useState(false);
    const [contestData, setContestData] = useState(null);
    const [standingsData, setStandingsData] = useState(null);

    const [refreshFlag, setRefreshFlag] = useState(new Date());
    useEffect(() => {
        const interval = setInterval(() => {
          setRefreshFlag(new Date());
        }, 4000);

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        getContest(accessToken, contestId).then(response => {
            if (response.success) {
                setContestData(response.data);
            } else setContestNotFound(true);
        });
        getStandings(accessToken, contestId).then(response => {
            if (response.success)
                setStandingsData(response.data);
        });
    }, [refreshFlag]);

    const isFullyLoaded = () => {
        return !(contestData === null || standingsData === null);
    }

    if (isContestNotFound)
        return <h1>Contest not found</h1>;

    if (!isFullyLoaded())
        return <Preloader/>;

    return (
        <div>
            <Typography variant="display2">
                {contestData.name}
            </Typography>
            <VWhitespace/>
            <Typography variant="subheading">
                Standings
            </Typography>
            <VWhitespace/>
            <Paper style={{marginTop: 8}} className={classes.paper}>
                <Table className={classes.table} padding="dense">
                    <TableHead>
                        <TableRow>
                            <TableCell>Username</TableCell>
                        {standingsData.tasks.map((data, index) => {
                            return <TableCell key={index}>{data.title}</TableCell>;
                        })}</TableRow>
                    </TableHead>
                    <TableBody>{standingsData.table.map((data, index) => {
                        return <TableRow key={index}>{data.map((cell, index2) => {
                            if (index2 === 0)
                                return <TableCell key={index2}>{cell.username}</TableCell>;
                            if (cell[0] === null || cell[0] === undefined)
                                return <TableCell key={index2}></TableCell>;
                            const style = {
                                background: cell[2]? lightGreen[300] : amber[300]
                            }
                            return <TableCell key={index2} style={style}>{cell[1]}</TableCell>;
                        })}</TableRow>;
                    })}</TableBody>
                </Table>
            </Paper>
        </div>
    );

}

export default withStyles(styles, { withTheme: true })(ContestStandingsPage);
