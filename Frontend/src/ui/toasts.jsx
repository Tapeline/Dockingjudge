import {toast} from "react-toastify";

export function toastError(message) {
    toast(<p style={{margin: 0}}>{message}</p>, {
        autoClose: 1500,
        type: "error",
        position: "bottom-left"
    });
}

export function toastSuccess(message) {
    toast(<p style={{margin: 0}}>{message}</p>, {
        autoClose: 1000,
        type: "success",
        position: "bottom-left"
    });
}
