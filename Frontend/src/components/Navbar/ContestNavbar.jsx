import dockingjudgeWhite from "../../assets/dockingjudgeWhite.png";
import React, {useEffect, useState} from "react";
import {NavLink, useNavigate, useParams} from "react-router-dom";
import {getContest} from "../../api/endpoints-contests.jsx";
import ContestPageLink from "./ContestPageLink.jsx";
import {
    AppBar,
    Button,
    CircularProgress,
    Divider,
    Drawer,
    Hidden,
    List, ListItem, ListItemIcon, ListItemText,
    Typography,
    withStyles
} from "@material-ui/core";
import Navbar from "./Navbar.jsx";
import {Edit, Settings} from "@material-ui/icons";

const styles = theme => ({
    root: {
        flexGrow: 1,
        height: 440,
        zIndex: 1,
        overflow: 'hidden',
        position: 'relative',
        display: 'flex',
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
    },
    drawerPaper: {
        position: 'relative',
        width: 240,
        height: "100vh"
    },
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing.unit * 3,
        minWidth: 0, // So the Typography noWrap works
    },
    toolbar: theme.mixins.toolbar,
});

function ContestNavbar(props) {
    const {classes, theme} = props;
    const {contestId} = useParams();
    const [contestData, setContestData] = useState(null);
    const [isMobileDrawerOpen, setIsMobileDrawerOpen] = useState(false);

    const navigate = useNavigate();

    useEffect(() => {
        getContest(localStorage.getItem("accessToken"), contestId).then(response => {
            if (response.success) setContestData(response.data);
        });
    }, []);

    const drawer = (
        <div>
            <div className={classes.toolbar}/>
            <div style={{padding: 16}}>
                <Typography variant="headline">
                    {contestData?.name}
                </Typography>
                <Typography variant="subheading">
                    {contestData?.description}
                </Typography>
            </div>
            <Divider />
            <List>{
                    contestData?.pages?.map(data => {
                        return <ContestPageLink contestId={contestId}
                                                closeCallback={() => setIsMobileDrawerOpen(false)}
                                                data={data}/>;
                    })
            }</List>
            <Divider/>
            <List>
                {
                    contestData?.author == localStorage.getItem("accountId")
                        ? <ListItem button
                                    onClick={() => {
                                        navigate(`/contests/${contestId}/edit`);
                                        setTimeout(() => setIsMobileDrawerOpen(false), 100);
                                    }}>
                            <ListItemIcon><Settings/></ListItemIcon>
                            <ListItemText primary="Settings"/>
                        </ListItem>
                        : ""
                }
            </List>
        </div>
    );

    const drawerToggleHandler = () => setIsMobileDrawerOpen(!isMobileDrawerOpen);

    if (contestData === null)
        return <CircularProgress className={classes.progress}/>;

    return (<>
        <Navbar hasDrawer drawerToggleHandler={drawerToggleHandler}/>
        <Hidden mdUp>
            <Drawer
                variant="temporary"
                anchor={theme.direction === 'rtl' ? 'right' : 'left'}
                open={isMobileDrawerOpen}
                onClose={drawerToggleHandler}
                classes={{
                    paper: classes.drawerPaper,
                }}
                ModalProps={{
                    keepMounted: true, // Better open performance on mobile.
                }}
            >
                {drawer}
            </Drawer>
        </Hidden>
        <Hidden smDown implementation="css">
            <Drawer
                variant="permanent"
                open
                classes={{
                    paper: classes.drawerPaper,
                }}
            >
                {drawer}
            </Drawer>
        </Hidden>
    </>);
}

export default withStyles(styles, { withTheme: true })(ContestNavbar);
