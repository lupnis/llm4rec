const { defineConfig } = require('@vue/cli-service')

const HOSTNAME = "localhost";
const HOSTPORT = "8000";
require('events').EventEmitter.defaultMaxListeners = 0;
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api/user/login" : {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/user/vlogin": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/user/logout": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/user/info": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/game/search": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/game/recommend": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/chat/create": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/chat/stop": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/chat/verify": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/chat/chat": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
      "/api/chat/history": {
        "target": `http://${HOSTNAME}:${HOSTPORT}/`,
        "secure": false,
        "changeOrigin": true
      },
    }
  }
})

