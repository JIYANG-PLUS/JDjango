/**
 * 利用 LocalStorage 读写客户端缓存
 * 
 * 使用方式（参照）localStorage 只是别名，可任取
 * import localStorage from '../utils/localStorage'
 * 然后再具体的方法内部：
 * console.log(localStorage.readByKey('jy'))
 */

export default {
    readByKey(key, default_v='[]') {
        return JSON.parse(window.localStorage.getItem(key) || default_v)
    },
    writeValueByKey(key, value) {
        window.localStorage.setItem(key, JSON.stringify(value))
    }
}
