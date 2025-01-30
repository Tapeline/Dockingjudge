export function getHost() {
    if (import.meta.env.DEV)
        return "http://localhost:8888";
    return "https://dockingjudge.tapeline.dev";
}

export function getBaseUrl() {
    ///const envUrl = import.meta.env.API_BASE_URL;
    // console.log(import.meta.env.API_BASE_URL, import.meta.env.API_WS_URL);
    // console.log(import.meta.env);
    // console.log(JSON.stringify(import.meta.env));
    // //if (envUrl === null || envUrl === undefined)
    // if (import.meta.env.DEV)
    //     return "http://localhost:8888/api/v1/";
    // return "https://dockingjudge.tapeline.dev/api/v1/";
    return `${getHost()}/api/v1/`;
}

export function apiUrl(url) {
    return getBaseUrl() + url;
}


export function s3Url(url) {
    return getHost() + url;
}


import axios from 'axios';


export async function sendRequest(method, url, data = null, headers = {}) {
    try {
        const response = await axios({
            method: method,
            url: url,
            data: data,
            headers: headers
        })
        return {success: true, data: response.data};
    } catch (error) {
        return {
            success: false,
            status: error.response.status,
            reason: error.response.data.detail,
            errorCode: error.response.data.code,
            data: error
        };
    }
}
