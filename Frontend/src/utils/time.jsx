const pad = n => `${Math.floor(Math.abs(n))}`.padStart(2, '0');
// Get timezone offset in ISO format (+hh:mm or -hh:mm)
const getTimezoneOffset = date => {
    const tzOffset = -date.getTimezoneOffset();
    const diff = tzOffset >= 0 ? '+' : '-';
    return diff + pad(tzOffset / 60) + ':' + pad(tzOffset % 60);
};

export const toISOStringWithTimeZone = date => {
    return date.getFullYear() +
        '-' + pad(date.getMonth() + 1) +
        '-' + pad(date.getDate()) +
        'T' + pad(date.getHours()) +
        ':' + pad(date.getMinutes()) +
        ':' + pad(date.getSeconds()) +
        getTimezoneOffset(date);
};

export function dateConverter(isoDate) {
    if (isoDate === null) {
        return ""
    }
    const dateObj = new Date(isoDate);
    const hours = String(dateObj.getHours());
    const minutes = String(dateObj.getMinutes()).padStart(2, '0');
    const day = String(dateObj.getDate());
    const month = String(dateObj.getMonth() + 1);
    const year = String(dateObj.getFullYear());
    const formattedDate = `${hours}:${minutes} ${day}/${month}/${year}`;
    return formattedDate;
}
