import {useEffect, useState} from "react";
import {Button, Form, Tab, Tabs} from "react-bootstrap";
import {toastError, toastSuccess} from "../../ui/toasts.jsx";
import {useNavigate, useParams} from "react-router-dom";
import {
    deleteProfile,
    getProfile, modifyProfileSettings, setUserProfilePic
} from "../../api/endpoints-accounts.jsx";
import ConfirmDeletionDialog from "../../components/Dialogs/ConfirmDeletionDialog/ConfirmDeletionDialog.jsx";
import VWhitespace from "../../utils/VWhitespace.jsx";
import CategoryPanel from "../../components/CategorySwitcher/CategoryPanel.jsx";
import CategorySwitcher from "../../components/CategorySwitcher/CategorySwitcher.jsx";
import Preloader from "../../components/Preloader/Preloader.jsx";
import ProfilePic from "../../components/Misc/ProfilePic.jsx";

export default function ProfilePage() {
    const {page} = useParams();
    const [key, setKey] = useState(page);
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const [profileData, setProfileData] = useState(null);
    const [profilePic, setProfilePic] = useState();

    if (page === null) {
        navigate("/profile/dashboard");
        return;
    }

    useEffect(() => {
        getProfile(accessToken).then(response => {
            setProfileData(response.data);
        });
    }, []);

    useEffect(() => {
        navigate("/profile/" + key + "/");
    }, [key]);


    if (profileData === null)
        return <Preloader/>;

    const onProfilePicSubmit = (e) => {
        if (profilePic === undefined) {
            toastError("Profile picture not defined");
            return;
        }
        setUserProfilePic(accessToken, profilePic).then(response => {
            window.location.href = "/profile/manage/#pfp";
        });
    }

    const onAccountDelete = () => {
        deleteProfile(accessToken).then((response) => {
            if (!response.success) toastError(response.reason);
            else window.location.href = "/";
        });
    };

    return (<div className="px-lg-5">
        <h1>Your profile</h1>
        <VWhitespace size={1}/>

        <Tabs id="controlled-tab-example" activeKey={key}
              onSelect={(k) => setKey(k)} className="mb-3">
            <Tab eventKey="dashboard" title="Dashboard">
                Nothing here now
            </Tab>
            <Tab eventKey="manage" title="Manage">
                <CategorySwitcher defaultKey="#general">
                    <CategoryPanel name="General" tabId="#general">
                        <h4>Username: {profileData.username}</h4>
                        <h6>ID: {profileData.id}</h6>
                    </CategoryPanel>
                    <CategoryPanel name="Profile Picture" tabId="#pfp">
                        <p>Current profile pic</p>
                        <ProfilePic url={profileData.profile_pic} size={128}/>
                        <VWhitespace/>
                        <Form.Control
                            type="file"
                            name="profile_pic"
                            accept="image/jpeg,image/png,image/gif"
                            onChange={(e) => setProfilePic(e.target.files[0])}
                        />
                        <VWhitespace/>
                        <Button variant="outline-primary" onClick={onProfilePicSubmit}>
                            Set profile picture
                        </Button>
                    </CategoryPanel>
                    <CategoryPanel name="Danger zone" tabId="#danger-zone">
                        <ConfirmDeletionDialog
                            buttonText="Delete account"
                            header="Delete account?"
                            text={<>
                                Are you sure you want to delete your account?<br/>
                                <b>This action is not undoable, proceed with caution!</b>
                            </>}
                            onOk={onAccountDelete}
                        />
                    </CategoryPanel>
                </CategorySwitcher>
            </Tab>
        </Tabs>
    </div>);
}
