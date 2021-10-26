// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import echarts from 'echarts'
import VueSession from 'vue-session'

Vue.prototype.$echarts = echarts
Vue.config.productionTip = false
Vue.use(VueSession)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router, // 一个简化的写法，完整的写法是 router:router (key/value 一模一样，则可以简写)
  components: { App }, // 声明一个组件 App，App 这个组件在一开始已经导入到项目中了，但是直接导入的组件无法直接使用，必须要声明
  template: '<App/>' // template 中定义了页面模板，即将 App 组件中的内容渲染到 '#app' 这个div 中
})
