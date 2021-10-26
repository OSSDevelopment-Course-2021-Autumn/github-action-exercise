import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import OpenStack from '@/components/OpenStack'
import Company from '@/components/Company'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'OpenStack',
      component: OpenStack
    },
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/company/:comp_name',
      name: 'Company',
      component: Company
    }
  ]
})
