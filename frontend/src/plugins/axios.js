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
    return response;
}, async (error) => {
    let request = error.config
    if (error.response.status == 401) {
        if (!request._retry && request.url != "auth/refresh") {
            request._retry = true
            const { data: { access_token } } = await instance.post("auth/refresh", { "refresh_token": localStorage.getItem("refresh_token") })
            localStorage.setItem("access_token", access_token)
            return instance(request)
        } else {
            router.push("/login")
        }
    } else if (error.response.status == 404) {
        // TODO: add alert
        console.error("Not found");
    }
    return Promise.reject(error);
});

export default instance
