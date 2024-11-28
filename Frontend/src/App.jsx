import './App.css'
import {Outlet, useLocation, useNavigate} from "react-router-dom";
import Navbar from "./components/Navbar/Navbar.jsx";
import {useEffect, useState} from "react";
import {getProfile} from "./api/endpoints-accounts.jsx";
import Preloader from "./components/Preloader/Preloader.jsx";
import ContestNavbar from "./components/Navbar/ContestNavbar.jsx";
import {CssBaseline, withStyles} from "@material-ui/core";
import locales from "./locales.jsx";
import {localSettings, valueOr} from "./utils/localSettings.jsx";

const styles = theme => ({
    root: {
        display: 'flex',
    },
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        minWidth: 0,
        minHeight: '100vh',
        paddingTop: 80
    }
});

function App(props) {
    const [isAuthorized, setIsAuthorized] = useState(null);
    const token = localStorage.getItem("accessToken");
    const navigate = useNavigate();
    const location = useLocation();
    const {classes, theme} = props;

    if (token === null || token === undefined)
        navigate("/login");

    locales.setLanguage(valueOr(localSettings.getStr("locale"), "en"));

    useEffect(() => {
        getProfile(localStorage.getItem("accessToken")).then(response => {
            const tokenInvalid = !response.success && response.status === 401;
            if (!tokenInvalid) {
                localStorage.setItem("accountUsername", response.data.username);
                localStorage.setItem("accountId", response.data.id);
            }
            setIsAuthorized(!tokenInvalid);
        })
    }, []);

    if (isAuthorized === null) return <Preloader/>;
    if (!isAuthorized) navigate("/login");

    if (location.pathname === "/") navigate("/contests");

    return (<>
        <CssBaseline />
        <div className={classes.root}>
            {location.pathname.startsWith("/contests/")
                ? <ContestNavbar/>
                : <Navbar/>}
            <main id="content" className={classes.content}>
                <Outlet/>
            </main>
        </div>
    </>);
}

export default withStyles(styles, { withTheme: true })(App);

