import router from "@/router"
import axios from "axios"

const instance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        common: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    }
})

instance.interceptors.request.use((config) => {
    config.headers['Authorization'] = `Bearer ${localStorage.getItem("access_token")}`
    return config
}, (error) => {
    return Promise.reject(error)
})

instance.interceptors.response.use((response) => {
    return response
}, (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401) {
        if (!originalRequest._retry && error.config.url != "/auth/refresh") {
            originalRequest._retry = true;
            let access_token = ""
            instance
                .post("/auth/refresh", {
                    "refresh_token": localStorage.getItem("refresh_token")
                })
                .then((resp) => {
                    console.log(resp.data)
                    access_token = resp.data.access_token
                    localStorage.setItem("access_token", access_token)
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
                });
            return instance(originalRequest);
        }
        router.push("/login")
    } else if (error.response.status === 422) {
        console.log(error);
    }
    return Promise.reject(error);
})

export default instance
