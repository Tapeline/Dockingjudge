import {apiUrl, sendRequest} from "./common.jsx";

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
        apiUrl(`solutions/for-task/quiz/${taskId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getQuizSolution(token, solutionId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/get/quiz/${solutionId}/`),
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
        apiUrl(`solutions/for-task/code/${taskId}/`),
        {},
        "Authorization: Bearer " + token
    )
}

export function getCodeSolution(token, solutionId) {
    return sendRequest(
        "GET",
        apiUrl(`solutions/get/code/${solutionId}/`),
        {},
        "Authorization: Bearer " + token
    )
}
