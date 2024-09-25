import {useState} from "react";
import {login, register} from "../../api/endpoints-accounts.jsx";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import {Link, useNavigate} from "react-router-dom";
import dockingjudgeBlue from "../../assets/dockingjudgeBlue.png";
import VWhitespace from "../../utils/VWhitespace.jsx";
import appStorage from "../../utils/appStorage.jsx";
import {FormControl, Input, InputLabel, Paper, Typography, withStyles, Button} from "@material-ui/core";
import HWhitespace from "../../utils/HWhitespace.jsx";

const styles = theme => ({
    layout: {
        width: 'auto',
        marginLeft: theme.spacing.unit * 3,
        marginRight: theme.spacing.unit * 3,
        [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
            width: 400,
            marginLeft: 'auto',
            marginRight: 'auto',
        },
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    paper: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: `${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
    },
    avatar: {
        margin: theme.spacing.unit,
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        marginTop: theme.spacing.unit,
    },
    submit: {
        marginTop: theme.spacing.unit * 3,
    },
});

function LoginPage(props) {
    const [userName, setUserName] = useState("");
    const [userPass, setUserPass] = useState("");
    const navigate = useNavigate();
    const {theme, classes} = props;

    const handleSubmit = (e) => {
        e.preventDefault();
        register(userName, userPass).then(response => {
            if (!response.success) {
                toastError(response.reason);
            } else {
                toastSuccess("Successfully registered");
                login(userName, userPass).then(response => {
                    if (!response.success) {
                        toastError(response.reason);
                    } else {
                        localStorage.setItem("accessToken", response.data.token);
                        navigate("/");
                    }
                })
            }
        }).catch(toastError);
    }

    return (
        <main className={classes.layout}>
            <Paper className={classes.paper}>
                <img src={dockingjudgeBlue} alt="Logo" style={{width: "320px"}}/>
                <Typography variant="headline">Register</Typography>
                <form className={classes.form} onSubmit={handleSubmit}>
                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="username">Login</InputLabel>
                        <Input
                            id="username"
                            name="username"
                            autoComplete="username"
                            onChange={e => setUserName(e.target.value)}
                            autoFocus
                        />
                    </FormControl>
                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="password">Password</InputLabel>
                        <Input
                            name="password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            onChange={e => setUserPass(e.target.value)}
                        />
                    </FormControl>
                    <Button
                        type="submit"
                        fullWidth
                        variant="raised"
                        color="primary"
                        className={classes.submit}
                    >
                        Register
                    </Button>
                    <VWhitespace/>
                    <Typography variant="caption">
                        Already have an account? Then use <Link to="/login">login</Link>
                    </Typography>
                </form>
            </Paper>
        </main>
    )
}

export default withStyles(styles, {withTheme: true})(LoginPage);
