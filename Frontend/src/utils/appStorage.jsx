const appStorage = {
    saveUserData: (data) => {
        localStorage.setItem("accountUsername", data.username);
        localStorage.setItem("accountId", data.id);
    }
}

export default appStorage;
