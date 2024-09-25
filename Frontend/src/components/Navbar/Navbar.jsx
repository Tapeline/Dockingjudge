import React, {useEffect, useState} from "react";
import dockingjudgeWhite from "../../assets/dockingjudgeWhite.png";
import {AppBar, Toolbar, Typography, Button, withStyles, IconButton} from "@material-ui/core";
import {AccountCircle, Help, Home, Menu, Settings} from "@material-ui/icons";

const styles = {};

function Navbar(props) {
    const {hasDrawer, drawerToggleHandler, classes, theme} = props;
    const [isMobile, setIsMobile] = useState(false);

    const handleResize = () => {
        setIsMobile(window.innerWidth < 960);
    }

    useEffect(() => {
        handleResize();
    }, []);

    useEffect(() => {
        window.addEventListener("resize", handleResize);
        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, []);

    return (
        <AppBar position="absolute" className={classes.appBar} style={{zIndex: 10000}}>
            <Toolbar style={{justifyContent: "space-between"}}>
                <div>
                    {
                        hasDrawer && isMobile
                            ? <IconButton
                                color="inherit"
                                aria-label="Open drawer"
                                onClick={drawerToggleHandler}
                                className={classes.navIconHide}>
                                <Menu/>
                            </IconButton>
                            : ""
                    }
                    {
                        isMobile
                            ? ""
                            : <img src={dockingjudgeWhite} alt="Logo" style={{
                                height: 32,
                                marginRight: 32
                            }}/>
                    }
                </div>
                <div>
                    <Button color="inherit" href="/contests">
                        {
                            isMobile
                                ? <Home/>
                                : "Contests"
                        }
                    </Button>
                    <Button color="inherit" href="/local-settings">
                        {
                            isMobile
                                ? <Settings/>
                                : "Settings"
                        }
                    </Button>
                    <Button color="inherit" href="/help">
                        {
                            isMobile
                                ? <Help/>
                                : "Help"
                        }
                    </Button>
                    <Button color="inherit" href="/profile">
                        {
                            isMobile
                                ? <AccountCircle/>
                                : "Profile"
                        }
                    </Button>
                </div>
            </Toolbar>
        </AppBar>
    );
}

export default withStyles(styles, {withTheme: true})(Navbar);
