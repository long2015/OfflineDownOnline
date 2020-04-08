// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
let Base64 = require('js-base64').Base64
import VueWorker from 'vue-worker'

Vue.use(VueWorker)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  data: {
    url: '',
    result: '',
    download_url: '',
    show: false,

    worker: null
  },
  methods: {
    submit: function (event) {
      if (this.url === '') {
        alert('地址不能为空')
        return false
      }
      let base64Url = Base64.encode(this.url)
      console.log('download_url:' + this.url + 'base:' + base64Url)
      // vue-resource
      this.result = 'Donwloading...'
      url = 'http://149.129.112.221/offlinedown---' + base64Url + '111---1'
      this.worker = this.$worker.run(() => url)
        .then(function (url){
            console.log(url)
            axios.get(url).then(res => {
            // success callback
            this.result = '下载成功.'
            this.download_url = res.data['download_url']
            this.show = true
          }, err => {
            // error callback
            this.result = '下载失败!!'
            this.show = false
            console.log(err)
          })
        })
    }
  }
})
