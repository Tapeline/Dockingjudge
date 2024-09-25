import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import Preloader from "../../components/Preloader/Preloader.jsx";
import {getAllContests} from "../../api/endpoints-contests.jsx";
import ContestCard from "../../components/ContestCard/ContestCard.jsx";
import CreateContestDialog from "../../components/Dialogs/CreateContestDialog/CreateContestDialog.jsx";
import {CircularProgress, Typography, withStyles} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";

const styles = theme => ({});

function ContestListPage(props) {
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [contestList, setContestList] = useState(null);
    const {classes, theme} = props;

    useEffect(() => {
        getAllContests(accessToken).then(response => {
            setContestList(response.data);
        });
    }, []);

    return (
        contestList === null?
        <CircularProgress className={classes.progress}/>
        :
        <div>
            <Typography variant="display2" style={{marginBottom: 16}}>
                All contests
                <HWhitespace width={1}/>
                <CreateContestDialog/>
            </Typography>
            {
                contestList?.map(function (data, id) {
                    return <ContestCard key={id} data={data}/>;
                })
            }
        </div>
    );
}

export default withStyles(styles, { withTheme: true })(ContestListPage);
