import axios from 'axios'

const request = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
    timeout: 12000, // 两分钟
    headers: {
        'Content-Type': 'aplication/json',
        'Accept': 'application/json',
    }
})

// 请求拦截器
request.interceptors.request.use(
    config => {
        config.headers['token'] = ''
        return config
    },
    error => {
      return Promise.reject(error)
    }
  )

// 响应拦截器


export default request
