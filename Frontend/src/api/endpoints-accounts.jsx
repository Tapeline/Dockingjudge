import {apiUrl, sendRequest} from "./common.jsx";

export function login(username, password) {
    return sendRequest(
        "POST",
        apiUrl("accounts/login/"),
        {
            username: username,
            password: password
        }
    )
}

export function register(username, password) {
    return sendRequest(
        "POST",
        apiUrl("accounts/register/"),
        {
            username: username,
            password: password
        }
    )
}

export function getProfile(token) {
    return sendRequest(
        "GET",
        apiUrl("accounts/profile/"),
        {},
        "Authorization: Bearer " + token
    )
}

export function modifyProfileSettings(token, newSettings) {
    return sendRequest(
        "PATCH",
        apiUrl("accounts/profile/"),
        {"settings": newSettings},
        "Authorization: Bearer " + token
    )
}

export function deleteProfile(token) {
    return sendRequest(
        "DELETE",
        apiUrl("accounts/profile/"),
        {},
        "Authorization: Bearer " + token
    )
}

export function setUserProfilePic(token, picFile) {
    const formData = new FormData();
    formData.append("profile_pic", picFile, picFile.name);
    return sendRequest(
        "PATCH",
        apiUrl("accounts/profile/pic/"),
        formData,
        {
            "Authorization": "Bearer " + token,
            "Content-Type": "multipart/form-data"
        }
    );
}

