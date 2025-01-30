import {apiUrl, s3Url, sendRequest} from "./common.jsx";
import axios from "axios";

export function submitQuizSolution(token, taskId, text) {
    return sendRequest(
        "POST",
        apiUrl(`solutions/post/quiz/${taskId}/`),
        {text: text},
        "Authorization: Bearer " + token
    )
}

export function getQuizSolutions(token, taskId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/my/quiz/${taskId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getQuizSolution(token, solutionId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/${solutionId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function submitCodeSolution(token, taskId, text, compiler, format) {
    return sendRequest(
        "POST",
        apiUrl(`solutions/post/code/${taskId}/`),
        {text: text, compiler: compiler, submission_type: format},
        "Authorization: Bearer " + token
    )
}

export function getCodeSolutions(token, taskId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/my/code/${taskId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getCodeSolution(token, solutionId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/${solutionId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getCodeFile(url) {
    return axios.get(s3Url(url),{responseType: 'text'})
}

export function getStandings(token, contestId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/standings/${contestId}/`),
        {},
        "Authorization: Bearer " + token
    )
}
