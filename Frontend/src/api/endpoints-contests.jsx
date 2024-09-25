import {apiUrl, sendRequest} from "./common.jsx";

export function getAllContests(token) {
    return sendRequest(
        "GET",
        apiUrl("contests/"),
        {},
        "Authorization: Bearer " + token
    )
}

export function getContest(token, contestId) {
    return sendRequest(
        "GET",
        apiUrl(`contests/${contestId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function createContest(token, data) {
    return sendRequest(
        "POST",
        apiUrl(`contests/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function modifyContest(token, contestId, data) {
    return sendRequest(
        "PATCH",
        apiUrl(`contests/${contestId}/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function deleteContest(token, contestId) {
    return sendRequest(
        "DELETE",
        apiUrl(`contests/${contestId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getContestPage(token, contestId, pageType, pageId) {
    return sendRequest(
        "GET",
        apiUrl(`contests/${contestId}/tasks/${pageType}/${pageId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function tryToEnterContest(token, contestId) {
    return sendRequest(
        "POST",
        apiUrl(`contests/${contestId}/apply/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getAvailableCompilers() {
    return sendRequest(
        "GET",
        apiUrl(`contests/compilers/`),
        {}
    )
}

export function modifyQuizPage(token, contestId, pageId, data) {
    return sendRequest(
        "PATCH",
        apiUrl(`contests/${contestId}/tasks/quiz/${pageId}/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function modifyCodePage(token, contestId, pageId, data) {
    return sendRequest(
        "PATCH",
        apiUrl(`contests/${contestId}/tasks/code/${pageId}/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function modifyTextPage(token, contestId, pageId, data) {
    return sendRequest(
        "PATCH",
        apiUrl(`contests/${contestId}/tasks/text/${pageId}/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function deleteQuizPage(token, contestId, pageId) {
    return sendRequest(
        "DELETE",
        apiUrl(`contests/${contestId}/tasks/quiz/${pageId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function deleteCodePage(token, contestId, pageId) {
    return sendRequest(
        "DELETE",
        apiUrl(`contests/${contestId}/tasks/code/${pageId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function deleteTextPage(token, contestId, pageId) {
    return sendRequest(
        "DELETE",
        apiUrl(`contests/${contestId}/tasks/text/${pageId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function createQuizPage(token, contestId, data) {
    return sendRequest(
        "POST",
        apiUrl(`contests/${contestId}/tasks/quiz/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function createCodePage(token, contestId, data) {
    return sendRequest(
        "POST",
        apiUrl(`contests/${contestId}/tasks/code/`),
        data,
        "Authorization: Bearer " + token
    )
}

export function createTextPage(token, contestId, data) {
    return sendRequest(
        "POST",
        apiUrl(`contests/${contestId}/tasks/text/`),
        data,
        "Authorization: Bearer " + token
    )
}