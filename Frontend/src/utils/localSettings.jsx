export function getBoolSetting(key) {
    return localStorage.getItem("ls_" + key) === "true";
}

export function setBoolSetting(key, value) {
    return localStorage.setItem("ls_" + key, (value === true).toString());
}

export function getStrSetting(key) {
    return localStorage.getItem("ls_" + key);
}

export function setStrSetting(key, value) {
    return localStorage.setItem("ls_" + key, value);
}

export function valueOr(value, defaultValue) {
    if (value === null || value === undefined)
        return defaultValue;
    return value;
}

export const localSettings = {
    getBool: getBoolSetting,
    setBool: setBoolSetting,
    setStr: setStrSetting,
    getStr: getStrSetting,
    valueOr: valueOr
};
